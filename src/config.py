import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


class Config:
    FLASK_ENV = os.getenv("FLASK_ENV", "development")

    # Database credentials and configuration
    DEV_DB_USER = os.getenv("DEV_DB_USER", "postgres")
    DEV_DB_PASSWORD = os.getenv("DEV_DB_PASSWORD", "password")
    DEV_DATABASE_NAME = os.getenv("DEV_DATABASE_NAME", "mydatabase")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")

    CLOUD_SQL_CONNECTION_NAME = os.getenv("DEV_CONNECTION_NAME")

    # SQLAlchemy Database URI (either local or Cloud SQL based on environment)
    if os.getenv("FLASK_ENV") == "production":
        # Cloud SQL connection URI for production (using Cloud SQL Proxy)
        SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DEV_DB_USER}:{DEV_DB_PASSWORD}@/{DEV_DATABASE_NAME}?host=/cloudsql/{CLOUD_SQL_CONNECTION_NAME}"
    else:
        # Local PostgresSQL URI for development
        SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DEV_DB_USER}:{DEV_DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DEV_DATABASE_NAME}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False


db = SQLAlchemy()
