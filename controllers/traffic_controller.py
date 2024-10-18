import cv2
from models.yolov8_model import TrafficModel

# Define average vehicle emissions (g CO2/km)
VEHICLE_EMISSIONS = {
    'auto': 70,
    'bus': 900,
    'tempo': 150,
    'tractor': 700,
    'truck': 800,
    'car': 120,
    'motorcycle': 60,
    'emergency': 150  # Assuming an average value for emergency vehicles
}

class TrafficController:
    def __init__(self, model_path='yolov8n.pt'):
        self.model = TrafficModel(model_path)

    def process_traffic_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        frame_count = 0
        total_vehicles = 0
        total_emissions = 0
        emergency_vehicles = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            if frame_count % 30 != 0:  # Process every 30th frame
                continue

            results = self.model.detect(frame)
            processed_results = self.model.process_results(results)
            
            for detection in processed_results:
                vehicle_type = detection['class']
                confidence = detection['score']
                
                if confidence > 0.5:  # Confidence threshold
                    total_vehicles += 1
                    total_emissions += VEHICLE_EMISSIONS.get(vehicle_type, 0)
                    if vehicle_type == 'emergency':
                        emergency_vehicles += 1

        cap.release()

        return self.decide_traffic_light(total_vehicles, total_emissions, emergency_vehicles)

    def decide_traffic_light(self, vehicle_count, total_emissions, emergency_vehicles):
        if emergency_vehicles > 0:
            return 'green'
        elif vehicle_count > 10 or total_emissions > 5000:
            return 'green'
        else:
            return 'red'

# Create an instance of the controller to make the function accessible globally
traffic_controller = TrafficController()

# Create a wrapper to expose the method directly
def process_traffic_video(video_path):
    return traffic_controller.process_traffic_video(video_path)
