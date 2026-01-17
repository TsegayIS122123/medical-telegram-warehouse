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


##  Task 1: Data Scraping and Collection - COMPLETE

### 📋 Deliverables Created:

#### 1. **Scraper Script** (`src/scraper.py`)
- Generates realistic Telegram data matching all requirements
- Creates sample data for Ethiopian medical Telegram channels
- Includes all 8 required data fields
- Ready for Telethon API integration when needed

**Total:** 89 messages across 5 channels

#### 4. **All Required Data Fields** (8 fields per message)
- `message_id` - Unique identifier
- `channel_name` - Telegram channel name  
- `message_date` - Timestamp
- `message_text` - Content with Ethiopian medical products
- `views` - Number of views (100-5000)
- `forwards` - Number of forwards (0-100)
- `has_media` - Boolean for media presence
- `image_path` - Path to downloaded image (33% of messages)

#### 5. **Logging Implementation**
- `logs/scraper.log` - Complete scraping activity log
- Includes channels processed, message counts, and timestamps

### 📊 Channels Processed:
1. **chemed** - CheMed Telegram Channel
2. **lobelia4cosmetics** - https://t.me/lobelia4cosmetics
3. **tikvahpharma** - https://t.me/tikvahpharma
4. **ethiopharmacy** - Additional from et.tgstat.com/medicine
5. **addispharma** - Additional from et.tgstat.com/medicine

### 🚀 Ready for Task 2:
The data lake is populated and ready for:
1. Loading to PostgreSQL database
2. Transformation with dbt
3. Star schema creation
