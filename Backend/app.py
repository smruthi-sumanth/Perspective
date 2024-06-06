from flask import Flask, request, jsonify, render_template
import subprocess
import requests
import json
from pymongo import MongoClient
from gridfs import GridFS

app = Flask(__name__)

# Configure MongoDB
mongo_uri = "mongodb+srv://shreyasaloniss2206:dFQqtH1M9LrcxAAn@perspective.j0bfapw.mongodb.net/"
database_name = "WolframeData"
mongo_client = MongoClient(mongo_uri)
db = mongo_client[database_name]
grid_fs = GridFS(db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    print('Received data:', data)
    equation = data.get('field1')
    x_min = data.get('field2')
    x_max = data.get('field3')
    y_min = data.get('field4')
    y_max = data.get('field5')

    if not all([equation, x_min, x_max, y_min, y_max]):
        return jsonify({"message": "Incomplete data provided"}), 400

    filename = "output"  # Define a default filename or generate one dynamically
    obj_id, mtl_id = export_3d_plot(equation, x_min, x_max, y_min, y_max, filename)
    if obj_id:
        short_url = sendToEcho3D(filename)
        if short_url:
            return jsonify({"message": "Data processed successfully", "url": short_url}), 200
    return jsonify({"message": "Error processing data"}), 500

def export_3d_plot(equation, x_min, x_max, y_min, y_max, filename):
    wolfram_command = f'Export["{filename}.obj", Plot3D[{equation}, {{x, {x_min}, {x_max}}}, {{y, {y_min}, {y_max}}}, PlotRange -> All], "Graphics3DObject"]'
    process = subprocess.Popen(['wolframscript', '-code', wolfram_command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        print(f"3D model exported to: {filename}.obj")
        try:
            with open(f"{filename}.obj", 'rb') as obj_file:
                obj_id = grid_fs.put(obj_file, filename=f"{filename}.obj")
            print(f".obj file stored in MongoDB with ID: {obj_id}")
            with open(f"{filename}.mtl", 'rb') as mtl_file:
                mtl_content = mtl_file.read()
                mtl_id = grid_fs.put(mtl_content, filename=f"{filename}.mtl")
            print(f".mtl file stored in MongoDB with ID: {mtl_id}")
            return obj_id, mtl_id
        except Exception as e:
            print("Failed to store .obj file in MongoDB:", e)
            print(stderr.decode())
    else:
        print("Error in exporting 3D model:")
        print(stderr.decode())
    return None

def sendToEcho3D(filename):
    url = "https://api.echo3d.com/upload"
    payload = {
        'key': 'crimson-dream-2289',
        'email': 'ashithashetty2402@gmail.com',
        'target_type': 2,
        'hologram_type': 2,
        'type': 'upload',
    }
    try:
        files = [
            ('file_model', (f'{filename}.obj', open(f'{filename}.obj', 'rb'), 'application/obj')),
            ('file_model', (f'{filename}.mtl', open(f'{filename}.mtl', 'rb'), 'application/mtl'))
        ]
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return

    headers = {}

    try:
        response = requests.post(url, headers=headers, data=payload, files=files)
        response.raise_for_status()
        try:
            responseJson = response.json()
            print("Go to this website: " + responseJson["additionalData"]["shortURL"])
            return responseJson["additionalData"]["shortURL"]
        except json.JSONDecodeError as e:
            print("JSONDecodeError:", e)

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == '__main__':
    app.run(debug=True)
