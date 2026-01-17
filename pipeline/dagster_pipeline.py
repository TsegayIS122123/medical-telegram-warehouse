# pipeline/dagster_pipeline.py - COMPLETE DAGSTER PIPELINE
from dagster import job, op, get_dagster_logger, schedule
from datetime import datetime
import subprocess
import os
import sys

logger = get_dagster_logger()

@op
def scrape_telegram_data():
    """Run Telegram scraper"""
    logger.info("🔄 Starting Telegram data scraping...")
    
    try:
        result = subprocess.run(
            [sys.executable, "src/scraper.py"],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        if result.returncode == 0:
            logger.info("✅ Telegram scraping completed successfully")
            return {
                "status": "success",
                "message": "Scraped Telegram data",
                "output": result.stdout[-500:]  # Last 500 chars
            }
        else:
            logger.error(f"❌ Telegram scraping failed: {result.stderr}")
            raise Exception(f"Scraping failed: {result.stderr}")
            
    except Exception as e:
        logger.error(f"❌ Error in scraping: {e}")
        raise

@op
def load_raw_to_postgres(context, scrape_result):
    """Load raw data to PostgreSQL"""
    logger.info("🔄 Loading data to PostgreSQL...")
    
    try:
        result = subprocess.run(
            [sys.executable, "src/loader.py"],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        if result.returncode == 0:
            logger.info("✅ Data loaded to PostgreSQL successfully")
            return {
                "status": "success",
                "message": "Data loaded to PostgreSQL",
                "scrape_result": scrape_result,
                "output": result.stdout[-500:]
            }
        else:
            logger.error(f"❌ Data loading failed: {result.stderr}")
            raise Exception(f"Loading failed: {result.stderr}")
            
    except Exception as e:
        logger.error(f"❌ Error in loading: {e}")
        raise

@op
def run_dbt_transformations(context, load_result):
    """Run dbt transformations"""
    logger.info("🔄 Running dbt transformations...")
    
    try:
        # Run dbt
        dbt_run = subprocess.run(
            ["dbt", "run"],
            capture_output=True,
            text=True,
            cwd="medical_warehouse"
        )
        
        # Run dbt tests
        dbt_test = subprocess.run(
            ["dbt", "test"],
            capture_output=True,
            text=True,
            cwd="medical_warehouse"
        )
        
        if dbt_run.returncode == 0 and dbt_test.returncode == 0:
            logger.info("✅ dbt transformations completed successfully")
            return {
                "status": "success",
                "message": "dbt transformations complete",
                "load_result": load_result,
                "dbt_output": dbt_run.stdout[-500:] + "\n" + dbt_test.stdout[-500:]
            }
        else:
            error_msg = f"dbt run: {dbt_run.stderr}\ndbt test: {dbt_test.stderr}"
            logger.error(f"❌ dbt transformations failed: {error_msg}")
            raise Exception(f"dbt failed: {error_msg}")
            
    except Exception as e:
        logger.error(f"❌ Error in dbt: {e}")
        raise

@op
def run_yolo_enrichment(context, dbt_result):
    """Run YOLO object detection"""
    logger.info("🔄 Running YOLO object detection...")
    
    try:
        result = subprocess.run(
            [sys.executable, "src/yolo_detect.py"],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        if result.returncode == 0:
            logger.info("✅ YOLO enrichment completed successfully")
            
            # Create final summary
            summary = {
                "status": "success",
                "message": "Pipeline execution complete",
                "timestamp": datetime.now().isoformat(),
                "stages": {
                    "scraping": dbt_result["load_result"]["scrape_result"]["status"],
                    "loading": dbt_result["load_result"]["status"],
                    "dbt": dbt_result["status"],
                    "yolo": "success"
                },
                "output": result.stdout[-500:]
            }
            
            logger.info(f"📊 Pipeline Summary: {summary}")
            return summary
            
        else:
            logger.error(f"❌ YOLO enrichment failed: {result.stderr}")
            raise Exception(f"YOLO failed: {result.stderr}")
            
    except Exception as e:
        logger.error(f"❌ Error in YOLO: {e}")
        raise

@job
def medical_telegram_pipeline():
    """Main pipeline for Medical Telegram Warehouse"""
    scrape_result = scrape_telegram_data()
    load_result = load_raw_to_postgres(scrape_result)
    dbt_result = run_dbt_transformations(load_result)
    run_yolo_enrichment(dbt_result)

@schedule(
    cron_schedule="0 2 * * *",  # Daily at 2 AM
    job=medical_telegram_pipeline,
    execution_timezone="UTC"
)
def daily_pipeline_schedule(context):
    """Schedule pipeline to run daily"""
    logger.info(f"📅 Scheduled pipeline execution: {context.scheduled_execution_time}")
    return {}

# For manual execution
if __name__ == "__main__":
    # Test pipeline locally
    result = medical_telegram_pipeline.execute_in_process()
    
    if result.success:
        print("✅ Pipeline execution successful!")
        print(f"Run ID: {result.run_id}")
    else:
        print("❌ Pipeline execution failed")
        print(f"Error: {result.failure_data}")