import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

database_user = os.getenv("DB_USER")
database_password = os.getenv("DB_PASSWORD")
database_name = os.getenv("DATABASE_NAME")


class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql://{database_user}:{database_password}@localhost:5432/{database_name}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


db = SQLAlchemy()
