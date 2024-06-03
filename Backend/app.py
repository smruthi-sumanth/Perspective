import subprocess
import requests
import json

def export_3d_plot(equation, x_min, x_max, y_min, y_max, filename):
    # Define the Wolfram command with the given parameters
    wolfram_command = f'Export["{filename}.obj", Plot3D[{equation}, {{x, {x_min}, {x_max}}}, {{y, {y_min}, {y_max}}}, PlotRange -> All], "Graphics3DObject"]'

    # Run the Wolfram command using subprocess
    result = subprocess.run(['wolframscript', '-code', wolfram_command], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"3D model exported to: {filename}.obj")
    else:
        print("Error in exporting 3D model:")
        print(result.stderr)

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
    y_max = float(input("Enter the maximum value for y: "))
    filename = input("Enter the output filename (without .obj extension): ")

    export_3d_plot(equation, x_min, x_max, y_min, y_max, filename)
    sendToEcho3D()

