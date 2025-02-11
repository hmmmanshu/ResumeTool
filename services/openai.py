from openai import OpenAI
import config
from models import OpenAIFile, OpenAIThread
from models import db


def generate_text(prompt, thread_id, assistant_id, file=None, user_id=None):
    client = OpenAI(api_key=config.Config.OPENAI_API_KEY)
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

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id, assistant_id=assistant_id
    )
    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        return str(messages.data[0].content[0].text.value)
    else:
        print(run.status)
        print(run.last_error)


def upload_file_to_openai(file, user_id):
    print("Creating new file")
    client = OpenAI(api_key=config.Config.OPENAI_API_KEY)
    file_id = client.files.create(
        file=(file.filename, file.stream, file.mimetype), purpose="assistants"
    ).id

    new_file = OpenAIFile(id=file_id, user_id=user_id)
    db.session.add(new_file)
    db.session.commit()
    print("New file id saved to db")

    return file_id


def create_thread(user_id):
    print("Creating new thread")
    client = OpenAI(api_key=config.Config.OPENAI_API_KEY)
    thread_id = client.beta.threads.create().id

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
