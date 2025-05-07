from flask import Flask
from flask_migrate import Migrate
from src.config import Config
from src.model.models import db
from src.router.angi_integration import app as angi_blueprint
from src.custom_exception import (
    BadRequestException,
    NotFoundException,
    ForbiddenException,
    ConflictException,
)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(angi_blueprint)

    # Exception handling
    @app.errorhandler(BadRequestException)
    def handle_bad_request(error):
        return error.to_response()

    @app.errorhandler(NotFoundException)
    def handle_not_found(error):
        return error.to_response()

    @app.errorhandler(ForbiddenException)
    def handle_forbidden(error):
        return error.to_response()

    @app.errorhandler(ConflictException)
    def handle_conflict(error):
        return error.to_response()

    @app.get("/")
    def hello_world():
        return "Hello, World!"

    return app


# For running the server
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
