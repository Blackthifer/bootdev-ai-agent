import os

def write_file(working_directory, file_path, content):
    f_path = os.path.realpath(os.path.join(os.path.abspath(working_directory), file_path))
    wd_path = os.path.abspath(working_directory)
    if wd_path not in f_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(f_path):
        os.makedirs(os.path.split(f_path)[0], exist_ok=True)
        open(f_path, "w").close()
    if not os.path.isfile(f_path):
        return f'Error: Path is not a regular file: "{file_path}"'
    try:
        file = open(f_path, "w")
        written = file.write(content)
        file.close()
    except Exception as e:
        return f"Error: {e}"
    return f'Successfully wrote to "{file_path}" ({written} characters written)'