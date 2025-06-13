import os

def get_file_content(working_directory, file_path):
    f_path = os.path.realpath(os.path.join(os.path.abspath(working_directory), file_path))
    wd_path = os.path.abspath(working_directory)
    if not os.path.isfile(f_path) or not os.path.exists(f_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    if wd_path not in f_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    try:
        file = open(f_path)
        output = ""
        output += file.read(10000)
        if file.tell() >= 10000:
            output += f'[...File "{file_path}" truncated at 10000 characters]'
        file.close()
    except Exception as e:
        return f"Error: {e}"
    return output
