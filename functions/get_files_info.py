import os

def get_files_info(working_directory, directory=None):
    if directory is None:
        return f'Error: "{directory}" is not a directory'
    wd_path = os.path.abspath(working_directory)
    d_path = os.path.realpath(os.path.join(wd_path, directory))
    if not os.path.isdir(d_path) or not os.path.exists(d_path):
        return f'Error: "{directory}" is not a directory'
    if wd_path not in d_path:
        return f'Error: cannot list "{directory}" as it is outside the permitted working directory'
    try:
        dir_contents = os.listdir(d_path)
        output = ""
        for content in dir_contents:
            content_path = os.path.join(d_path, content)
            output += f"{content}: file_size={os.path.getsize(content_path)} bytes, is_dir={os.path.isdir(content_path)}\n"
    except Exception as e:
        return f"Error: {e}"
    return output