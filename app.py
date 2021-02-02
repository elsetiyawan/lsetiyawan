from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger

import os
import datetime

from databases.db import db
from databases.models import User, Files
from resources.UserController import UserController
from resources.FileController import FileController
from resources.AuthController import AuthController

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    "DATABASE_URI", "postgresql://elsetiyawan:1123581321@localhost/elsetiyawan")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET")
app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER")

logger = get_task_logger(__name__)

jwt = JWTManager(app)

db.init_app(app)

api = Api(app)

api.add_resource(UserController, "/api/v1/users")
api.add_resource(AuthController, "/api/v1/login")
api.add_resource(FileController, "/api/v1/files")


# celery
def make_celery(app):
    app.config['CELERYBEAT_SCHEDULE'] = {
        # Executes every minute
        'periodic_task-every-minute': {
            'task': 'periodic_task',
            'schedule': crontab(minute="*")
        }
    }

    celery = Celery(app.import_name, broker='amqp://localhost')
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


celery = make_celery(app)


@celery.task(name="periodic_task")
def periodic_task():
    files = Files.query.all()
    for file in files:
        process_doc.delay(file.id, file.path)
    logger.info("Processing periodic task")


@celery.task(name="process_doc")
def process_doc(id, path):
    text = open(path, "r").read().lower()
    count = 0
    listScore = [
        {"text": "secret", "score": 10},
        {"text": "dathena", "score": 7},
        {"text": "internal", "score": 5},
        {"text": "external", "score": 3},
        {"text": "public", "score": 1}
    ]

    for x in listScore:
        if x["text"] in text:
            count += x["score"]

    file = Files.query.filter_by(id=id).first()
    file.score = count
    db.session.commit()

    print(count)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
