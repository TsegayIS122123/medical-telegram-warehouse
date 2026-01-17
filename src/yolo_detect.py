# src/yolo_detect.py - COMPLETE YOLO DETECTION
import os
import csv
import pandas as pd
from pathlib import Path
from ultralytics import YOLO
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YOLODetector:
    def __init__(self):
        # Load YOLOv8 nano model (small & fast)
        self.model = YOLO('yolov8n.pt')
        
        # Define detection classes we care about
        self.person_classes = ['person']
        self.product_classes = ['bottle', 'cup', 'vase', 'handbag', 'cell phone', 'laptop']
        
        # Output file
        self.output_csv = 'data/yolo_detections.csv'
        
        # Create directories
        os.makedirs('data', exist_ok=True)
        os.makedirs('logs', exist_ok=True)
    
    def classify_image(self, detections):
        """Classify image based on detected objects"""
        detected_objects = [det['class_name'] for det in detections]
        
        has_person = any(obj in self.person_classes for obj in detected_objects)
        has_product = any(obj in self.product_classes for obj in detected_objects)
        
        if has_person and has_product:
            return 'promotional'
        elif has_product and not has_person:
            return 'product_display'
        elif has_person and not has_product:
            return 'lifestyle'
        else:
            return 'other'
    
    def detect_image(self, image_path, message_id, channel_name):
        """Run YOLO detection on single image"""
        try:
            # Run detection
            results = self.model(image_path, verbose=False)
            
            detections = []
            confidence_scores = []
            
            # Extract detections
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        class_id = int(box.cls[0])
                        class_name = self.model.names[class_id]
                        confidence = float(box.conf[0])
                        
                        detections.append({
                            'class_id': class_id,
                            'class_name': class_name,
                            'confidence': confidence
                        })
                        confidence_scores.append(confidence)
            
            # Classify image
            image_category = self.classify_image(detections)
            
            # Get top detection
            top_detection = max(detections, key=lambda x: x['confidence']) if detections else None
            
            return {
                'message_id': message_id,
                'channel_name': channel_name,
                'image_path': image_path,
                'detected_class': top_detection['class_name'] if top_detection else 'none',
                'confidence_score': top_detection['confidence'] if top_detection else 0.0,
                'image_category': image_category,
                'detection_count': len(detections),
                'detected_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error detecting {image_path}: {e}")
            return None
    
    def process_all_images(self):
        """Process all images from Task 1"""
        logger.info("🔍 Starting YOLO object detection...")
        
        all_results = []
        images_dir = Path('data/raw/images')
        
        if not images_dir.exists():
            logger.error(f"Images directory not found: {images_dir}")
            return []
        
        # Find all images
        image_count = 0
        for channel_dir in images_dir.iterdir():
            if channel_dir.is_dir():
                channel_name = channel_dir.name
                
                for image_file in channel_dir.glob('*.jpg'):
                    # Extract message_id from filename
                    try:
                        message_id = int(image_file.stem)
                    except ValueError:
                        message_id = hash(image_file.stem) % 1000000
                    
                    # Run detection
                    result = self.detect_image(
                        str(image_file),
                        message_id,
                        channel_name
                    )
                    
                    if result:
                        all_results.append(result)
                        image_count += 1
                        
                        if image_count % 5 == 0:
                            logger.info(f"  Processed {image_count} images...")
        
        # Save to CSV
        if all_results:
            df = pd.DataFrame(all_results)
            df.to_csv(self.output_csv, index=False)
            logger.info(f"✅ Saved {len(all_results)} detections to {self.output_csv}")
            
            # Show summary
            self.show_summary(df)
        else:
            logger.warning("⚠️ No images processed")
        
        return all_results
    
    def show_summary(self, df):
        """Show detection summary"""
        print("\n" + "="*60)
        print("📊 YOLO DETECTION SUMMARY")
        print("="*60)
        
        print(f"\n📁 Total images processed: {len(df)}")
        
        # By category
        print("\n🖼️ Image Categories:")
        for category, count in df['image_category'].value_counts().items():
            percentage = (count / len(df)) * 100
            print(f"  {category}: {count} images ({percentage:.1f}%)")
        
        # By channel
        print("\n📡 By Channel:")
        for channel, group in df.groupby('channel_name'):
            cat_counts = group['image_category'].value_counts()
            print(f"  {channel}: {len(group)} images")
            for cat, count in cat_counts.items():
                print(f"    - {cat}: {count}")
        
        # Top detected objects
        print("\n🎯 Top Detected Objects:")
        top_objects = df['detected_class'].value_counts().head(5)
        for obj, count in top_objects.items():
            print(f"  {obj}: {count} times")
        
        print("\n" + "="*60)
    
    def load_to_postgres(self):
        """Load YOLO results to PostgreSQL"""
        try:
            import psycopg2
            
            # Read CSV
            df = pd.read_csv(self.output_csv)
            
            # Connect to PostgreSQL
            conn = psycopg2.connect(
                host="localhost",
                database="medical_warehouse",
                user="postgres",
                password="postgres",
                port="5433"
            )
            
            cur = conn.cursor()
            
            # Create table
            cur.execute("""
            CREATE TABLE IF NOT EXISTS raw.yolo_detections (
                id SERIAL PRIMARY KEY,
                message_id INTEGER,
                channel_name VARCHAR(255),
                image_path TEXT,
                detected_class VARCHAR(100),
                confidence_score FLOAT,
                image_category VARCHAR(50),
                detection_count INTEGER,
                detected_at TIMESTAMP
            );
            """)
            
            # Insert data
            for _, row in df.iterrows():
                cur.execute("""
                INSERT INTO raw.yolo_detections 
                (message_id, channel_name, image_path, detected_class, 
                 confidence_score, image_category, detection_count, detected_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
                """, (
                    row['message_id'],
                    row['channel_name'],
                    row['image_path'],
                    row['detected_class'],
                    row['confidence_score'],
                    row['image_category'],
                    row['detection_count'],
                    row['detected_at']
                ))
            
            conn.commit()
            cur.close()
            conn.close()
            
            logger.info(f"✅ Loaded {len(df)} detections to raw.yolo_detections")
            
        except Exception as e:
            logger.error(f"❌ Error loading to PostgreSQL: {e}")

def main():
    """Main function"""
    print("\n" + "="*60)
    print("🎯 YOLOv8 OBJECT DETECTION - TASK 3")
    print("="*60)
    
    detector = YOLODetector()
    
    # Step 1: Process images
    results = detector.process_all_images()
    
    if results:
        # Step 2: Load to PostgreSQL
        detector.load_to_postgres()
        
        print("\n✅ TASK 3 COMPLETE!")
        print("Next: Create dbt model fct_image_detections.sql")
        print("="*60)
    
    return results

if __name__ == "__main__":
    main()