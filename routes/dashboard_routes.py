from flask import Blueprint, render_template, request, session, redirect, url_for
from controllers.traffic_controller import process_traffic_video
from models.yolov8_model import TrafficModel
from flask import jsonify

dashboard_bp = Blueprint('dashboard', __name__)
traffic_model = TrafficModel('saved_models/final_yolo_finetuned.pt')

@dashboard_bp.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'user' not in session:
        return redirect(url_for('auth.login'))  # Redirect to login if not logged in

    # Render the dashboard, displaying all available junctions
    junctions = get_all_junctions()  # Fetch all junctions from the database
    return render_template('dashboard.html', junctions=junctions)

@dashboard_bp.route('/dashboard/junction/<int:id>')
def view_junction(id):
    junction = get_junction_by_id(id)  # Fetch junction info from the database
    return render_template('junction_dashboard.html', junction=junction)

@dashboard_bp.route('/dashboard/junction/<int:junction_id>/process', methods=['POST'])
def process_junction(junction_id):
    if 'video_path' not in request.files:
        return "No file part", 400

    video_file = request.files['video_path']
    if video_file.filename == '':
        return "No selected file", 400

    video_path = f"./uploads/{video_file.filename}"  # Define your upload path
    
    video_file.save(video_path)

    light_color = process_traffic_video(video_path)
    return jsonify({"light_color": light_color}), 200

@dashboard_bp.route('/dashboard/junction/<int:id>/manual_override', methods=['POST'])
def manual_override(id):
    # Logic to manually override traffic light at a specific junction
    light_color = request.form['light_color']
    update_traffic_light(id, light_color)
    return redirect(url_for('dashboard.view_junction', id=id))

def get_all_junctions():
    # Placeholder for actual logic to fetch all junctions from the database
    return [
        {'id': 1, 'name': 'Junction 1', 'lanes': 4},
        {'id': 2, 'name': 'Junction 2', 'lanes': 3},
    ]

def get_junction_by_id(junction_id):
    # Placeholder logic to fetch specific junction info
    return {'id': junction_id, 'name': f'Junction {junction_id}', 'lanes': 4}

def update_traffic_light(junction_id, color):
    # Logic to change the traffic light color at a junction (database update, etc.)
    print(f"Traffic light at junction {junction_id} set to {color}")
