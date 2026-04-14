from flask import Flask
from app.config import Config
from app.extensions import db, jwt, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(tasks_bp, url_prefix="/tasks")

    @app.get("/")
    def home():
        return {
            "message": "Task Manager API running successfully"
        }, 200

    return app
