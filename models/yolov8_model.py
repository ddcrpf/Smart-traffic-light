from ultralytics import YOLO
import torch

class TrafficModel:
    def __init__(self, model_path='yolov8n.pt'):
        self.model = YOLO(model_path)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.to(self.device)
        
        # Custom class names for Indian traffic
        self.class_names = ['auto', 'bus', 'tempo', 'tractor', 'truck', 'car', 'motorcycle', 'emergency']

    def detect(self, image):
        results = self.model(image, verbose=False)
        return results[0]  # Return the first (and only) result

    def process_results(self, results):
        processed_results = []
        for r in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = r
            class_name = self.class_names[int(class_id)] if int(class_id) < len(self.class_names) else 'unknown'
            processed_results.append({
                'bbox': [x1, y1, x2, y2],
                'score': score,
                'class': class_name
            })
        return processed_results