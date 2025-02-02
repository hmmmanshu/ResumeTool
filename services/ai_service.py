from openai import OpenAI
import config
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User

def generate_text(prompt, thread_id, file):
    # Thread id corresponse to a specific user's thread
    client = OpenAI(api_key=config.Config.OPENAI_API_KEY)
    assistant_id = config.Config.OPENAI_ASSISTANT_ID
    if file:
        file_id = upload_file_to_openai(file)
        print("file id", file_id)
        message = client.beta.threads.messages.create(thread_id=thread_id,role="user",content=prompt, attachments=[{'file_id': file_id, 'tools': [{"type": "file_search"}]}])
    else:
        message = client.beta.threads.messages.create(thread_id=thread_id,role="user",content=prompt)
        
    run = client.beta.threads.runs.create_and_poll(thread_id=thread_id, assistant_id=assistant_id)
    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
            thread_id=thread_id
        )
        return str(messages.data[0].content[0].text.value)
    else:
        print(run.status)


def upload_file_to_openai(file):
    client = OpenAI(api_key=config.Config.OPENAI_API_KEY)
    assistant_id = config.Config.OPENAI_ASSISTANT_ID
    response = client.files.create(
        file=(file.filename, file.stream, file.mimetype),
        purpose="assistants"
    )
    return response.id


def create_thread():
    # Create a thread for a new user
    client = OpenAI(api_key=config.Config.OPENAI_API_KEY)
    # TODO: add a try except here
    thread = client.beta.threads.create()
    print(f"Thread id, {thread.id}")
    return thread.id