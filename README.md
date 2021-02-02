docker build -t flaskapp .
docker-compose up -d
docker exec -it flaskapp /bin/bash
python manage.py db upgrade

docker exec -it flaskapp /bin/bash
celery -A app.celery beat

docker exec -it flaskapp /bin/bash
celery -A app.celery worker --loglevel=info