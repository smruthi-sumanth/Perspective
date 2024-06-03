import subprocess

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

# Example usage
if __name__ == "__main__":
    equation = input("Enter the equation (in terms of x and y): ")
    x_min = float(input("Enter the minimum value for x: "))
    x_max = float(input("Enter the maximum value for x: "))
    y_min = float(input("Enter the minimum value for y: "))
    y_max = float(input("Enter the maximum value for y: "))
    filename = input("Enter the output filename (without .obj extension): ")

    export_3d_plot(equation, x_min, x_max, y_min, y_max, filename)
