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

##  Task 2: Data Modeling and Transformation - COMPLETE

### 📊 Data Warehouse Implementation

#### Database: SQLite (`data/warehouse.db`)
We used SQLite for simplicity and ease of setup, creating a complete star schema data warehouse.

#### Schema Created:
raw_messages → clean_messages
↓
dim_channels + fact_messages

#### Tables Created:

##### 1. **raw_messages** (Raw Data Layer)
- Contains all 89 messages from Task 1 JSON files
- Preserves original data structure
- 8 columns: `message_id`, `channel_name`, `message_date`, `message_text`, `views`, `forwards`, `has_media`, `image_path`

##### 2. **clean_messages** (Staging/Cleaned Data)
- Cleaned and validated data
- Added calculated fields:
  - `message_length`: Length of message text
  - `has_image`: Boolean flag (1 if image exists)
- Filtered invalid records (null message_id, channel_name, or message_date)

##### 3. **dim_channels** (Dimension Table)
- Channel information and metrics
- Columns:
  - `channel_key`: Surrogate key (1-5)
  - `channel_name`: Original channel name
  - `channel_type`: Classified as Medical, Cosmetics, or Pharmaceutical
  - `total_posts`: Number of messages per channel
  - `avg_views`: Average views per post

##### 4. **fact_messages** (Fact Table)
- Core analytics table
- Columns:
  - `message_id`: Unique identifier
  - `channel_key`: Foreign key to dim_channels
  - `message_text`: Original message content
  - `message_length`: Text length
  - `view_count`: Number of views
  - `forward_count`: Number of forwards
  - `has_image`: Whether message contains an image

### 📋 Channel Classification Results:
| Channel | Type | Posts | Avg Views |
|---------|------|-------|-----------|
| addispharma | Pharmaceutical | 17 | ~2,550 |
| chemed | Medical | 17 | ~2,550 |
| ethiopharmacy | Pharmaceutical | 18 | ~2,550 |
| lobelia4cosmetics | Cosmetics | 22 | ~2,550 |
| tikvahpharma | Pharmaceutical | 15 | ~2,550 |

### 🛠️ How It Was Implemented:

#### Scripts Created:
1. **`scripts/load_data_simple.py`** - Main data loading script
2. **`scripts/check_tables_simple.py`** - Verification script

#### Commands to Run:
```bash
# Load data and create warehouse
python scripts/load_data_simple.py

# Verify results
python scripts/check_tables_simple.py