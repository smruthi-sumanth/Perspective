import subprocess
import requests
import json
from pymongo import MongoClient
from gridfs import GridFS

# Replace with your actual connection string and database name
mongo_uri = "mongodb+srv://shreyasaloniss2206:dFQqtH1M9LrcxAAn@perspective.j0bfapw.mongodb.net/"
database_name = "WolframeData"

mongo_client = MongoClient(mongo_uri)
db = mongo_client[database_name]
grid_fs = GridFS(db)


def export_3d_plot(equation, x_min, x_max, y_min, y_max, filename):
  wolfram_command = f'Export["{filename}.obj", Plot3D[{equation}, {{x, {x_min}, {x_max}}}, {{y, {y_min}, {y_max}}}, PlotRange -> All], "Graphics3DObject"]'

  process = subprocess.Popen(['wolframscript', '-code', wolfram_command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout, stderr = process.communicate()

  if process.returncode == 0:
    print(f"3D model exported to: {filename}.obj")
    try:
      obj_id = grid_fs.put(stdout, filename=f"{filename}.obj")  # Get the ID
      print(f".obj file stored in MongoDB with ID: {obj_id}")
      with open(f"{filename}.mtl", 'rb') as mtl_file:
        mtl_content = mtl_file.read()
      mtl_id = grid_fs.put(mtl_content, filename=f"{filename}.mtl")
      print(f".mtl file stored in MongoDB with ID: {mtl_id}")
      return obj_id, mtl_id 
    except Exception as e:
      print("Failed to store.obj file in MongoDB:", e)
      print(stderr.decode())
  else:
    print("Error in exporting 3D model:")
    print(stderr.decode())
  return None  # Indicate failure to retrieve ID


def sendToEcho3D():
    url = "https://api.echo3d.com/upload"  # Ensure the URL is correct
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
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        try:
            responseJson = response.json()
            print("Go to this website: " + responseJson["additionalData"]["shortURL"])
            return responseJson["additionalData"]["shortURL"]
        except json.JSONDecodeError as e:
            print("JSONDecodeError:", e)

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


# Example usage
if __name__ == "__main__":
  equation = input("Enter the equation (in terms of x and y): ")
  x_min = float(input("Enter the minimum value for x: "))
  x_max = float(input("Enter the maximum value for x: "))
  y_min = float(input("Enter the minimum value for y: "))
  y_max = float(input("Enter the minimum value for y: "))
  filename = input("Enter the output filename: ")

  obj_id, mtl_id = export_3d_plot(equation, x_min, x_max, y_min, y_max, filename)
  if obj_id:
    sendToEcho3D()
