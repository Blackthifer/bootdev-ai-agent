import os
import sys
from dotenv import load_dotenv
from google import genai

def main():
    arguments = sys.argv[1:]
    if len(arguments) < 1:
        print("No prompt given!\nusage: python main.py [prompt]")
        os._exit(1)
    load_dotenv()
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=gemini_api_key)
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=arguments[0])
    print(f"{response.text}\nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")

main()