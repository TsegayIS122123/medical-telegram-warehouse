import psycopg2

print("\n MEDICAL TELEGRAM WAREHOUSE - DATA VERIFICATION")
print("="*60)

try:
    # Connect to database
    conn = psycopg2.connect(
        host='localhost', 
        port=5433, 
        user='postgres', 
        password='postgres',
        database='medical_warehouse'
    )
    cur = conn.cursor()
    
    # First, check what columns exist in fct_messages
    cur.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_schema = 'public_marts' 
        AND table_name = 'fct_messages'
    """)
    columns = [col[0] for col in cur.fetchall()]
    print(f"\n Available columns: {columns}")
    
    # Check main tables
    cur.execute("SELECT COUNT(*) FROM public_marts.fct_messages")
    messages = cur.fetchone()[0]
    print(f"\n✅ Total Messages: {messages} rows")
    
    cur.execute("SELECT COUNT(*) FROM public_marts.fct_messages WHERE has_image = true")
    images = cur.fetchone()[0]
    print(f"✅ Messages with Images: {images} rows")
    
    # Check channels
    cur.execute("SELECT channel_name FROM public_marts.dim_channels")
    channels = cur.fetchall()
    print(f"✅ Channels: {len(channels)} - {[c[0] for c in channels]}")
    
    # Show sample messages - using the correct column names
    print("\n Sample Messages:")
    
    # Try different possible column names for channel
    channel_col = None
    for col in ['channel_name', 'channel', 'channelkey', 'channel_key']:
        if col in columns:
            channel_col = col
            break
    
    if channel_col:
        query = f"SELECT message_id, {channel_col}, message_text FROM public_marts.fct_messages LIMIT 3"
        cur.execute(query)
        samples = cur.fetchall()
        for msg_id, channel, text in samples:
            print(f"  [{channel}] {text[:50]}...")
    else:
        # If no channel column, just show message_id and text
        cur.execute("SELECT message_id, message_text FROM public_marts.fct_messages LIMIT 3")
        samples = cur.fetchall()
        for msg_id, text in samples:
            print(f"  [ID:{msg_id}] {text[:50]}...")
    
    # Check YOLO detections
    print("\n���️ YOLO Detection Summary:")
    try:
        cur.execute("SELECT COUNT(*) FROM public_public_marts.fct_image_detections")
        yolo_count = cur.fetchone()[0]
        print(f"  ✅ Images processed: {yolo_count}")
        
        if yolo_count > 0:
            cur.execute("""
                SELECT image_category, COUNT(*) 
                FROM public_public_marts.fct_image_detections 
                GROUP BY image_category
            """)
            categories = cur.fetchall()
            for category, count in categories:
                print(f"     - {category}: {count} images")
    except Exception as e:
        print(f"  ⚠️ Could not access YOLO table: {e}")
        # Check if YOLO CSV exists as fallback
        import os
        if os.path.exists('data/yolo_detections.csv'):
            import pandas as pd
            df = pd.read_csv('data/yolo_detections.csv')
            print(f"  ✅ YOLO CSV found: {len(df)} images")
            print(f"     Categories: {df['image_category'].value_counts().to_dict()}")
    
    cur.close()
    conn.close()
    print("\n" + "="*60)
    print("✅ VERIFICATION COMPLETE!")
    
except Exception as e:
    print(f"❌ Error: {e}")
