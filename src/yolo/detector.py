# src/yolo/detector.py
"""YOLO object detection module."""
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd
from ultralytics import YOLO
import logging
from datetime import datetime

from src.config import config
from src.yolo.classifier import ImageClassifier

logger = logging.getLogger(__name__)

class YOLODetector:
    """YOLO-based object detector for medical images."""
    
    def __init__(self):
        self.config = config.yolo
        self.model = YOLO(str(self.config.model_path))
        self.classifier = ImageClassifier()
        self.results = []
        
    def detect_image(self, image_path: Path, message_id: int, channel: str) -> Optional[Dict[str, Any]]:
        """
        Run detection on a single image.
        
        Args:
            image_path: Path to image file
            message_id: Associated message ID
            channel: Channel name
            
        Returns:
            Detection results dictionary or None if error
        """
        try:
            # Run detection
            results = self.model(image_path, verbose=False, conf=self.config.confidence_threshold)
            
            detections = []
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
                        
            # Classify image
            image_category = self.classifier.classify(detections)
            
            # Get top detection
            top_detection = max(detections, key=lambda x: x['confidence']) if detections else None
            
            return {
                'message_id': message_id,
                'channel_name': channel,
                'image_path': str(image_path),
                'detected_class': top_detection['class_name'] if top_detection else 'none',
                'confidence_score': top_detection['confidence'] if top_detection else 0.0,
                'image_category': image_category,
                'detection_count': len(detections),
                'detected_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error detecting {image_path}: {e}")
            return None
            
    def process_all_images(self) -> List[Dict[str, Any]]:
        """
        Process all images in the raw images directory.
        
        Returns:
            List of detection results
        """
        images_dir = Path("data/raw/images")
        
        if not images_dir.exists():
            logger.warning(f"Images directory not found: {images_dir}")
            return []
            
        self.results = []
        
        # Walk through channel directories
        for channel_dir in images_dir.iterdir():
            if not channel_dir.is_dir():
                continue
                
            channel = channel_dir.name
            
            for image_file in channel_dir.glob("*.jpg"):
                # Extract message ID from filename
                try:
                    message_id = int(image_file.stem)
                except ValueError:
                    # Fallback for non-numeric filenames
                    message_id = hash(image_file.stem) % 1000000
                    
                result = self.detect_image(image_file, message_id, channel)
                if result:
                    self.results.append(result)
                    
                if len(self.results) % 10 == 0:
                    logger.info(f"Processed {len(self.results)} images...")
                    
        logger.info(f"Completed processing {len(self.results)} images")
        return self.results
        
    def save_results(self, output_path: Path = Path("data/yolo_outputs/detections.csv")) -> None:
        """
        Save detection results to CSV.
        
        Args:
            output_path: Path to save CSV file
        """
        if not self.results:
            logger.warning("No results to save")
            return
            
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame(self.results)
        df.to_csv(output_path, index=False)
        logger.info(f"Saved {len(self.results)} detections to {output_path}")