import os
import subprocess

def run_python_file(working_directory, file_path):
    f_path = os.path.realpath(os.path.join(os.path.abspath(working_directory), file_path))
    wd_path = os.path.abspath(working_directory)
    if not f_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    if not os.path.isfile(f_path) or not os.path.exists(f_path):
        return f'Error: File "{file_path}" not found.'
    if wd_path not in f_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    try:
        result = subprocess.run("python " + f_path, timeout=30, capture_output=True, text=True)
        output = ""
        if not result.stdout == "":
            output += f"STDOUT: {result.stdout}\n"
        if not result.stderr == "":
            output += f"STDERR: {result.stderr}\n"
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}"
        if output == "":
            output += "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"
    return output