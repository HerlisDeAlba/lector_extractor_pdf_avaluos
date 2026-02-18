# src/gemini_service.py
import time
from google import genai
from google.genai import types
from . import config

def setup_client():
    """Configures and returns the Gemini Client."""
    return genai.Client(api_key=config.get_api_key())

def upload_file(client, path, mime_type="application/pdf"):
    """Uploads the given file to Gemini."""
    try:
        # Documentation: client.files.upload(file=path, config=...)
        file = client.files.upload(file=path, config={'mime_type': mime_type})
        print(f"Uploaded file '{file.name}' as: {file.uri}")
        return file
    except Exception as e:
        print(f"Upload failed: {e}")
        raise

def wait_for_file_active(client, file_obj):
    """Waits for the given file to be active."""
    print("Waiting for file processing...")
    file_name = file_obj.name
    file = client.files.get(name=file_name)
    while file.state == "PROCESSING":
        print(".", end="", flush=True)
        time.sleep(2)
        file = client.files.get(name=file_name)
    
    if file.state != "ACTIVE":
        raise Exception(f"File {file.name} failed to process with state: {file.state}")
    print("...file ready")

def generate_content(client, model, contents, response_mime_type="application/json"):
    """Wraps the generate_content call."""
    return client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type=response_mime_type
        )
    )
