import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    arguments = sys.argv[1:]
    if len(arguments) < 1:
        print("No prompt given!\nusage: python main.py [prompt] <options>\n")
        os._exit(1)
    if arguments[0] == "--help":
        print("usage: python main.py [prompt] <options>\nOptions:\n--verbose provides extra output")
        return
    load_dotenv()
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=gemini_api_key)
    config = generate_config(generate_function_schemas())
    print(ask_gemini(client, config, arguments))

def ask_gemini(client, config, arguments):
    messages = [ types.Content( role="user", parts=[ types.Part( text=arguments[0] ) ] ) ]
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages, config=config)
    output = ""
    if "--verbose" in arguments:
        output += f"User prompt: {arguments[0]}\n"
    output += compose_output(response, "--verbose" in arguments)
    return output

def compose_output(response, verbose = False):
    output = ""
    if verbose:
        output += f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n"
        output += f"Response tokens: {response.usage_metadata.candidates_token_count}\n\n"
    if response.text is not None:
        output += f"{response.text}\n"
    if response.function_calls is not None:
        for call in response.function_calls:
            output += call_function(call, verbose)
    return output

def call_function(function_call, verbose = False):
    output = f"Calling function: {function_call.name}"
    if verbose:
        output += f"({function_call.args})"
    return output + "\n"

def generate_config(functions):
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read files
- Write to or overwrite files
- Execute python files with optional arguments

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    return types.GenerateContentConfig(system_instruction=system_prompt, tools=[functions])

def generate_function_schemas():
    return types.Tool(function_declarations=[types.FunctionDeclaration(
                    name="get_files_info",
                    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
                    parameters=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "directory": types.Schema(
                                type=types.Type.STRING,
                                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself."
                            )
                        }
                    )
                ),
                types.FunctionDeclaration(
                    name="get_file_content",
                    description="Gets the contents from the specified file, truncated at 10000 characters, if the file is in the working directory.",
                    parameters=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "file_path": types.Schema(
                                type=types.Type.STRING,
                                description="The file path to read content from, relative to the working directory."
                            )
                        }
                    )
                ),
                types.FunctionDeclaration(
                    name="write_file",
                    description="Writes content to the specified file, overwriting the entirety of the file, if the file is in the working directory.",
                    parameters=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "file_path": types.Schema(
                                type=types.Type.STRING,
                                description="The file path to which to write the content, relative to the working directory."
                            ),
                            "content": types.Schema(
                                type=types.Type.STRING,
                                description="The content to overwrite the specified file with."
                            )
                        }
                    )
                ),
                types.FunctionDeclaration(
                    name="run_python_file",
                    description="Runs the specified file without arguments if it is a python file and in the working directory.",
                    parameters=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "file_path": types.Schema(
                                type=types.Type.STRING,
                                description="The file path of the file to run, relative to the working directory."
                            )
                        }
                    )
                )
            ])

main()