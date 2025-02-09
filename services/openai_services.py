from openai import OpenAI
import config
from models import OpenAIFile, OpenAIThread
from app import db


def generate_cover_letter(prompt, thread_id, file=None, user_id=None):
    client = OpenAI(api_key=config.Config.OPENAI_API_KEY)
    assistant_id = config.Config.OPENAI_ASSISTANT_COVER_LETTER_CREATE
    if file:
        file_id = upload_file_to_openai(file, user_id)
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=prompt,
            attachments=[{"file_id": file_id, "tools": [{"type": "file_search"}]}],
        )
    else:
        client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=prompt
        )

    cover_letter = execute_run(thread_id, assistant_id)
    return cover_letter


def upload_file_to_openai(file, user_id):
    # Create a file for a new user and save file_id to db
    print("Creating new file")
    client = OpenAI(api_key=config.Config.OPENAI_API_KEY)
    file_id = client.files.create(
        file=(file.filename, file.stream, file.mimetype), purpose="assistants"
    ).id

    # Add file_id to db
    new_file = OpenAIFile(id=file_id, user_id=user_id)
    db.session.add(new_file)
    db.session.commit()
    print("New file id saved to db")

    return file_id


def create_thread(user_id):
    # Create a thread for a new user and save thread_id to db
    print("Creating new thread")
    client = OpenAI(api_key=config.Config.OPENAI_API_KEY)
    thread_id = client.beta.threads.create().id

    # Add thread_id to db
    new_thread = OpenAIThread(id=thread_id, user_id=user_id)
    db.session.add(new_thread)
    db.session.commit()

    return thread_id


def delete_openai_file(file_id):
    client = OpenAI(api_key=config.Config.OPENAI_API_KEY)
    response = client.files.delete(file_id)
    print(f"File delete status :{response.deleted}")


def delete_openai_thread(thread_id):
    client = OpenAI(api_key=config.Config.OPENAI_API_KEY)
    response = client.beta.threads.delete(thread_id)
    print(f"Thread delete status :{response.deleted}")


def generate_resume_code(prompt, thread_id):
    client = OpenAI(api_key=config.Config.OPENAI_API_KEY)
    assistant_id = config.Config.OPENAI_ASSISTANT_RESUME_CREATE
    client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=prompt
    )
    latex_code = execute_run(thread_id, assistant_id)
    return latex_code


def execute_run(client, thread_id, assistant_id):
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id, assistant_id=assistant_id
    )
    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        return str(messages.data[0].content[0].text.value)
    else:
        print(run.status)
        print(run.last_error)
        return run.last_error
