import requests
import json

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
            ('file_model', ('ohforfeckssake.obj', open('ohforfeckssake.obj', 'rb'), 'application/obj')),
            ('file_model', ('ohforfeckssake.mtl', open('ohforfeckssake.mtl', 'rb'), 'application/mtl'))
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

sendToEcho3D()