import subprocess


wolfram_command = f'Export["C:\\Users\\User\\Desktop\\sine.obj", Plot3D{equation}, {x, -Pi, Pi}, {y, -Pi, Pi}], "Graphics3DObject"]'

# Run the Wolfram command using subprocess
subprocess.run(['wolframscript', '-code', wolfram_command])

print("3D model exported.")


