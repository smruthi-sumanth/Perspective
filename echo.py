import requests
import json


# The URL for the Echo3D upload API
url = 'https://api.echo3d.com/upload'

# Headers
headers = {}

# Prepare the data payload
payload = {
    'key': API_KEY,
    'email': USER_EMAIL,
    'target_type': TARGET_TYPE,
    'hologram_type': HOLOGRAM_TYPE,
    'type': TYPE,
}

# Specify the file paths
obj_file_path = 'C:\\Users\\User\\Desktop\\yoo.obj'
mtl_file_path = 'C:\\Users\\User\\Desktop\\yoo.mtl'

# Prepare the files for upload
files = [
    ('file_model', ('yoo.obj', open(obj_file_path, 'rb'), 'application/obj')),
    ('file_model', ('yoo.mtl', open(mtl_file_path, 'rb'), 'application/mtl'))
]

try:
    # Make the POST request
    response = requests.post(url, headers=headers, data=payload, files=files)
    
    # Check if the request was successful
    if response.status_code == 200:
        try:
            response_json = response.json()
            short_url = response_json["additionalData"].get("shortURL")
            if short_url:
                print("Go to this website: " + short_url)
            else:
                print("Upload succeeded, but no shortURL provided in response.")
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            print("Response content:", response.content)
    else:
        print("Request failed with status code:", response.status_code)
        print("Response content:", response.content)
except Exception as e:
    print("An error occurred during the file upload process:", e)
