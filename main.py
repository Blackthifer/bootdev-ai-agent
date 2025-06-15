import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def main():
    arguments = sys.argv[1:]
    if len(arguments) < 1:
        print("No prompt given!\nusage: python main.py [prompt] <options>")
        os._exit(1)
    if arguments[0] == "--help":
        print("usage: python main.py [prompt] <options>\nOptions:\n--verbose provides extra output")
        return
    load_dotenv()
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=gemini_api_key)
    config = generate_config(generate_function_schemas())
    ask_gemini(client, config, arguments)

def ask_gemini(client, config, arguments):
    verbose = "--verbose" in arguments
    messages = [ types.Content( role="user", parts=[ types.Part( text=arguments[0] ) ] ) ]
    response = None
    MAX_ITERATIONS = 20
    for _ in range(MAX_ITERATIONS):
        response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages, config=config)
        new_messages, iterate_again = handle_response(response, verbose)
        messages += new_messages
        if not iterate_again:
            break
    output = ""
    output += compose_output(arguments[0], response, verbose)
    print(output)

def handle_response(response, verbose):
    new_messages = []
    for candidate in response.candidates:
        new_messages += [candidate.content]
    function_called = False
    if response.function_calls is not None:
        for call in response.function_calls:
            call_result = call_function(call, verbose)
            if not (call_result.parts is not None and len(call_result.parts) > 0 and
                 call_result.parts[0].function_response is not None and
                 call_result.parts[0].function_response.response is not None):
                raise Exception("ERROR: INCORRECT FUNCTION CALL RETURN FORMAT")
            if verbose:
                print(f"-> {call_result.parts[0].function_response.response}")
            function_called = True
            new_messages += [call_result]
    return new_messages, function_called

def compose_output(prompt, response, verbose = False):
    output = ""
    if verbose:
        output += f"User prompt: {prompt}\n"
        output += f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n"
        output += f"Response tokens: {response.usage_metadata.candidates_token_count}\n\n"
    if response.text is not None:
        output += f"Final response:\n{response.text}"
    return output

def call_function(function_call, verbose = False):
    output = f"Calling function: {function_call.name}"
    if verbose:
        output += f"({function_call.args})"
    print(output)
    call_response = None
    function_dict = {"get_files_info": get_files_info, "get_file_content": get_file_content, "write_file": write_file, "run_python_file": run_python_file}
    if function_call.name in function_dict:
        function_call.args["working_directory"] = "./calculator"
        call_response = {"result": function_dict[function_call.name](**function_call.args)}
    else:
        call_response = {"error": f"Unknown function: {function_call.name}"}
    call_content = types.Content(role = "tool",
                                 parts = [types.Part.from_function_response(
                                   name = function_call.name,
                                   response = call_response
                                 )]
                                 )
    return call_content

def generate_config(functions):
    system_prompt = """
You are a helpful AI coding agent. You always provide a clear step-by-step explanation of what you've done and how things work.

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