# dashboard/app.py
"""Main Streamlit dashboard for Medical Telegram Analytics."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import text
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.connection import get_session
from src.config import config

# Page config
st.set_page_config(
    page_title="Medical Telegram Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("🏥 Ethiopian Medical Telegram Analytics")
st.markdown("Real-time insights from Ethiopian medical Telegram channels")

# Sidebar
st.sidebar.header("📊 Dashboard Controls")
st.sidebar.info(
    """
    This dashboard shows analytics from:
    - Chemed
    - Lobelia4Cosmetics
    - TikvahPharma
    """
)

# Database status
try:
    with get_session() as session:
        session.execute(text("SELECT 1"))
    st.sidebar.success("✅ Database Connected")
except Exception as e:
    st.sidebar.error(f"❌ Database Error: {str(e)}")

# Main metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    try:
        with get_session() as session:
            result = session.execute(text("SELECT COUNT(*) FROM public_marts.fct_messages")).scalar()
        st.metric("Total Messages", f"{result:,}")
    except:
        st.metric("Total Messages", "N/A")

with col2:
    try:
        with get_session() as session:
            result = session.execute(text("SELECT COUNT(*) FROM public_marts.fct_messages WHERE has_image = true")).scalar()
        st.metric("Images Analyzed", f"{result:,}")
    except:
        st.metric("Images Analyzed", "N/A")

with col3:
    try:
        with get_session() as session:
            result = session.execute(text("SELECT AVG(view_count) FROM public_marts.fct_messages")).scalar()
        st.metric("Avg Views/Message", f"{result:.0f}" if result else "0")
    except:
        st.metric("Avg Views/Message", "N/A")

with col4:
    try:
        with get_session() as session:
            result = session.execute(text("SELECT COUNT(*) FROM public_marts.dim_channels")).scalar()
        st.metric("Active Channels", result)
    except:
        st.metric("Active Channels", "N/A")

# Tabs for different views
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Overview", 
    "📦 Product Analysis", 
    "🖼️ Image Insights",
    "📊 YOLO Detection"
])

with tab1:
    st.header("Channel Activity Overview")
    
    try:
        with get_session() as session:
            query = text("""
            SELECT 
                c.channel_name,
                COUNT(f.message_id) as message_count,
                AVG(f.view_count) as avg_views
            FROM public_marts.fct_messages f
            JOIN public_marts.dim_channels c ON f.channel_key = c.channel_key
            GROUP BY c.channel_name
            ORDER BY message_count DESC
            """)
            df = pd.read_sql(query, session.bind)
        
        if not df.empty:
            fig = px.bar(
                df, 
                x='channel_name', 
                y='message_count',
                title='Messages per Channel',
                color='avg_views',
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available")
    except Exception as e:
        st.error(f"Error loading chart: {e}")

with tab2:
    st.header("Top Product Mentions")

    try:
        with get_session() as session:
            # SIMPLIFIED QUERY - extracts common words
            query = text("""
            SELECT 
                word,
                COUNT(*) as count
            FROM (
                SELECT 
                    regexp_split_to_table(LOWER(message_text), '[^a-z]+') as word
                FROM public_marts.fct_messages
                WHERE message_text IS NOT NULL 
                    AND message_text != ''
            ) words
            WHERE LENGTH(word) > 3
                AND word NOT IN ('the', 'and', 'for', 'with', 'from', 'this', 'that', 'are', 'was', 'were', 'has', 'have', 'not', 'you', 'your')
            GROUP BY word
            ORDER BY count DESC
            LIMIT 15
            """)
            df = pd.read_sql(query, session.bind)

        if not df.empty:
            fig = px.bar(
                df,
                x='count',
                y='word',
                orientation='h',
                title='Most Frequent Product-Related Words',
                labels={'count': 'Frequency', 'word': 'Word'}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No product data available")
    except Exception as e:
        st.error(f"Error loading products: {e}")
        # Show sample data for debugging
        with get_session() as session:
            sample = session.execute(text("SELECT message_text FROM public_marts.fct_messages LIMIT 3")).fetchall()
            st.write("Sample messages:", [s[0][:100] for s in sample])

with tab3:
    st.header("Image Content Analysis")
    
    try:
        with get_session() as session:
            # Get stats for messages with and without images
            query = text("""
            WITH stats AS (
                SELECT 
                    AVG(CASE WHEN has_image THEN view_count END) as avg_with_images,
                    AVG(CASE WHEN NOT has_image THEN view_count END) as avg_without_images,
                    COUNT(CASE WHEN has_image THEN 1 END) as images_count,
                    COUNT(DISTINCT CASE WHEN has_image THEN channel_key END) as channels_with_images
                FROM public_marts.fct_messages
            )
            SELECT * FROM stats
            """)
            stats = session.execute(query).first()
        
        if stats and stats.images_count > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                # Impact comparison
                fig = go.Figure(data=[
                    go.Bar(name='With Images', x=['Views'], y=[stats.avg_with_images or 0]),
                    go.Bar(name='Without Images', x=['Views'], y=[stats.avg_without_images or 0])
                ])
                fig.update_layout(
                    title='Impact of Images on Views',
                    barmode='group',
                    yaxis_title='Average Views'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                impact = ((stats.avg_with_images or 0) - (stats.avg_without_images or 0)) / (stats.avg_without_images or 1) * 100
                st.metric(
                    "Image Impact",
                    f"{impact:.1f}%",
                    delta=f"{impact:.1f}% more views with images"
                )
                st.metric("Images Analyzed", stats.images_count)
                st.metric("Channels Using Images", stats.channels_with_images)
        else:
            st.info("No image data available")
    except Exception as e:
        st.error(f"Error loading image stats: {e}")

with tab4:
    st.header("YOLO Object Detection Results")
    
    # Check if YOLO results exist
    yolo_file = 'data/yolo_detections.csv'
    if os.path.exists(yolo_file):
        df_yolo = pd.read_csv(yolo_file)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top detected objects
            top_objects = df_yolo['detected_class'].value_counts().head(10)
            if not top_objects.empty:
                fig = px.bar(
                    x=top_objects.values,
                    y=top_objects.index,
                    orientation='h',
                    title='Top 10 Detected Objects',
                    labels={'x': 'Count', 'y': 'Object'}
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Image categories
            categories = df_yolo['image_category'].value_counts()
            if not categories.empty:
                fig = px.pie(
                    values=categories.values,
                    names=categories.index,
                    title='Image Categories'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Confidence scores
        if 'confidence_score' in df_yolo.columns:
            st.subheader("Detection Confidence Distribution")
            fig = px.histogram(
                df_yolo, 
                x='confidence_score',
                nbins=20,
                title='Confidence Score Distribution'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Show raw data
        with st.expander("View Raw Detection Data"):
            st.dataframe(df_yolo)
    else:
        st.info("No YOLO detection results found. Run YOLO detection first.")