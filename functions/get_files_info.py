import os

def get_files_info(working_directory, directory=None):
    if not directory.startswith(working_directory):
        return f'Error: cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(directory) or not os.path.exists(directory):
        return f'Error: "{directory}" is not a directory'
    try:
        dir_contents = os.listdir(directory)
        output = ""
        for content in dir_contents:
            content_path = os.path.join(directory, content)
            output += f"{content}: file_size={os.path.getsize(content_path)} bytes, is_dir={os.path.isdir(content_path)}\n"
    except Exception as e:
        return f"Error: {e}"
    return output