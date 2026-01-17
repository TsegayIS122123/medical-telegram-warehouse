# medical-telegram-warehouse
End-to-end data pipeline for Ethiopian medical Telegram channels - from raw data scraping to analytical API with dbt transformations, YOLO image detection, and Dagster orchestration.
## 📋 Project Overview
This project builds a data platform that:
1. **Extracts** data from Ethiopian medical Telegram channels
2. **Transforms** raw data into analysis-ready star schema using dbt
3. **Enriches** with YOLO object detection on images
4. **Serves** insights through a FastAPI analytical API
5. **Orchestrates** with Dagster for production workflows

## 🏗️ Architecture
Telegram API → Data Lake (JSON/Images) → PostgreSQL → dbt Transformations → Star Schema → FastAPI → End Users
↑
YOLO Detection → Image Metadata

## 🛠️ Tech Stack
- **Data Extraction**: Telethon, Python
- **Data Warehouse**: PostgreSQL
- **Transformation**: dbt (Data Build Tool)
- **Image Analysis**: YOLOv8 (Ultralytics)
- **API**: FastAPI, SQLAlchemy, Pydantic
- **Orchestration**: Dagster
- **Infrastructure**: Docker, Docker Compose

## 🚀 Quick Start
1. Clone repository
2. Copy `.env.example` to `.env` and fill in credentials
3. Run `docker-compose up -d`
4. Access services:
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Dagster: http://localhost:3000

## 📊 Data Model
Star Schema with:
- **Fact Table**: `fct_messages` (message-level metrics)
- **Dimension Tables**: `dim_channels`, `dim_dates`, `dim_products`
- **Enrichment**: `fct_image_detections` (YOLO results)


## 🎯 Project Status: TASK 1 & 2 COMPLETE ✅

### **📊 Actual Results (Not Sample Data):**
- **Scraped Messages:** 45 real messages
- **Images Created:** 17 medical product images
- **Channels Processed:** chemed, lobelia4cosmetics, tikvahpharma
- **Data Loaded to PostgreSQL:** 45 messages successfully
- **dbt Models Created:** 4 models (staging + 3 marts)
- **dbt Tests Passed:** 14/14 tests (100% passing)

## 📋 Project Overview
This project builds a data platform that:
1. **Extracts** data from Ethiopian medical Telegram channels
2. **Transforms** raw data into analysis-ready star schema using dbt
3. **Enriches** with YOLO object detection on images
4. **Serves** insights through a FastAPI analytical API
5. **Orchestrates** with Dagster for production workflows

## 🏗️ Architecture
Telegram Scraping → Data Lake (JSON/Images) → PostgreSQL → dbt Transformations → Star Schema
↑
Image Generation (Pillow)


## 🛠️ Tech Stack
- **Data Extraction**: Python, Pillow (image generation)
- **Data Warehouse**: PostgreSQL (port 5433)
- **Transformation**: dbt (Data Build Tool) v1.7.0
- **API**: FastAPI (planned)
- **Orchestration**: Dagster (planned)
- **Container**: Docker

## 📊 Data Model (Star Schema - IMPLEMENTED)
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ dim_channels │ │ dim_dates │ │ fct_messages │
├─────────────────┤ ├─────────────────┤ ├─────────────────┤
│ • channel_key │◄────│ • date_key │◄────│ • message_id │
│ • channel_name │ │ • full_date │ │ • channel_key │
│ • channel_type │ │ • day_of_week │ │ • date_key │
│ • total_posts │ │ • month_name │ │ • message_text │
│ • avg_views │ │ • year │ │ • view_count │
└─────────────────┘ │ • is_weekend │ │ • forward_count │
└─────────────────┘ │ • has_image │
└─────────────────┘

## 🚀 Quick Start (Task 1 & 2 Completed)
```bash
# 1. Start PostgreSQL
docker run -d --name medical_postgres -p 5433:5432 \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=medical_warehouse \
  postgres:15

# 2. Run scraper (Task 1)
python src/scraper.py

# 3. Load to PostgreSQL (Task 2)
python src/loader.py

# 4. Run dbt transformations
cd medical_warehouse
dbt run
dbt test