from app import db
from services.openai import delete_openai_file, delete_openai_thread
from models import OpenAIFile, OpenAIThread

def wipe_user_session(user_id):
    wipe_user_threads(user_id)
    wipe_user_files(user_id)

def wipe_user_threads(user_id):
    print("Started thread wipe")
    threads = OpenAIThread.query.filter_by(user_id=user_id).all()
    for thread in threads:
        delete_openai_thread(thread.id)
        db.session.delete(thread)
    db.session.commit()

def wipe_user_files(user_id):
    print("Started file wipe")
    files = OpenAIFile.query.filter_by(user_id=user_id).all()
    for file in files:
        delete_openai_file(file.id)
        db.session.delete(file)
    db.session.commit()