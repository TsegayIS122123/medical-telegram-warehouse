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

