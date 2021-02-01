from .celery import celery
from databases.models import Files


@celery.task
def process_document(id, path):
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

    update = Files.query.filter_by(id=id).first()
    update.score = count
    db.session.commit()
