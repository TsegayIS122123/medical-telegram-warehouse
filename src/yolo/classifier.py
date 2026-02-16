# src/yolo/classifier.py
"""Image classification based on detected objects."""
from typing import List, Dict, Any

class ImageClassifier:
    """Classify images based on detected objects."""
    
    # Object categories
    PERSON_CLASSES = {'person'}
    PRODUCT_CLASSES = {'bottle', 'cup', 'vase', 'handbag', 'cell phone', 'laptop', 'book'}
    
    def classify(self, detections: List[Dict[str, Any]]) -> str:
        """
        Classify image based on detected objects.
        
        Args:
            detections: List of detected objects
            
        Returns:
            Image category: 'promotional', 'product_display', 'lifestyle', or 'other'
        """
        detected_objects = [d['class_name'] for d in detections]
        
        has_person = any(obj in self.PERSON_CLASSES for obj in detected_objects)
        has_product = any(obj in self.PRODUCT_CLASSES for obj in detected_objects)
        
        if has_person and has_product:
            return 'promotional'
        elif has_product and not has_person:
            return 'product_display'
        elif has_person and not has_product:
            return 'lifestyle'
        else:
            return 'other'