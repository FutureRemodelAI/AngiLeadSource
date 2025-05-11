import pytest
from app import create_app
from src.model.models import db
from src.config import Config

@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        # "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:postgres@localhost:5432/test",
        "SQLALCHEMY_DATABASE_URI": Config.SQLALCHEMY_DATABASE_URI,
        "SQLALCHEMY_TRACK_MODIFICATIONS": Config.SQLALCHEMY_TRACK_MODIFICATIONS,
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def db_session(app):
    """Creates a new database session for a test."""
    from sqlalchemy.orm import scoped_session, sessionmaker

    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()

        session_factory = sessionmaker(bind=connection)
        session = scoped_session(session_factory)

        db.session = session

        yield session

        transaction.rollback()
        connection.close()
        session.remove()
