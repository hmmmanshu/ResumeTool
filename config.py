import os
import configparser

# Read config file
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "options.cfg"))


class Config:
    SECRET_KEY = config["DEFAULT"]["SECRET_KEY"]
    JWT_SECRET_KEY = config["DEFAULT"]["JWT_SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = config["DEFAULT"]["SQLALCHEMY_DATABASE_URI"]
    S3_BUCKET = config["DEFAULT"]["S3_BUCKET"]
    S3_REGION = config["DEFAULT"]["S3_REGION"]
    OPENAI_API_KEY = config["DEFAULT"]["OPENAI_API_KEY"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AWS_ACCESS_KEY_ID = config["DEFAULT"]["AWS_ACCESS_KEY_ID"]
    AWS_SECRET_ACCESS_KEY = config["DEFAULT"]["AWS_SECRET_ACCESS_KEY"]
    OPENAI_ASSISTANT_ID = config["DEFAULT"]["OPENAI_ASSISTANT_ID"]
