import subprocess
from wolframclient.language import wl, wlexpr

def create_wolfram_command(equation, file_name):
    """
    Formats the Wolfram Language equation into a command for exporting a 3D plot as an OBJ file.

    Args:
        equation (str): The Wolfram Language mathematical equation.
        file_name (str): The desired file name for the exported OBJ file.

    Returns:
        str: The formatted Wolfram command.
    """
    # Format the Wolfram command
    wolfram_command = f'Export["C:\\Users\\User\\Desktop\\{file_name}.obj", Plot3D[{equation}, {{x, -Pi, Pi}}, {{y, -Pi, Pi}}], "Graphics3DObject"]'
    return wolfram_command

def export_3d_model(equation, file_name):
    """
    Executes the Wolfram command to export the 3D plot of the given equation as an OBJ file.

    Args:
        equation (str): The Wolfram Language mathematical equation to be plotted in 3D.
        file_name (str): The desired file name for the exported OBJ file.
    """
    # Create the Wolfram command
    wolfram_command = create_wolfram_command(equation, file_name)
    
    # Run the Wolfram command using subprocess
    try:
        subprocess.run(['wolframscript', '-code', wolfram_command], check=True)
        print(f"3D model exported to {file_name}.obj")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing the Wolfram command: {e}")


# User input for the natural language equation and file name
user_query = input("Enter the mathematical equation in wolfram: ")
file_name = input("Enter the desired file name for the OBJ file: ")
export_3d_model(user_query, file_name)
