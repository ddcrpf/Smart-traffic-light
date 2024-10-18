from flask import Flask, render_template, redirect, url_for
from config import Config
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from models.yolov8_model import TrafficModel
from controllers.traffic_controller import TrafficController

traffic_controller = TrafficController()
app = Flask(__name__)
app.config.from_object(Config)

# Load YOLOv8 model (loaded once globally)
traffic_model = TrafficModel('saved_models/final_yolo_finetuned.pt')

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

@app.route('/')
def home():
    # Render the home template
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
