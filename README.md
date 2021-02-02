**How to build**

build the image : 
```
docker build -t flaskapp .
```

docker compose :
```
docker-compose up -d
```

migrate database : 
```
docker exec -it flaskapp /bin/bash
python manage.py db upgrade
```

run the celery beat : 
```
open a new terminal
docker exec -it flaskapp /bin/bash
celery -A app.celery beat
```

run the celery worker : 
```
open a new terminal
docker exec -it flaskapp /bin/bash
celery -A app.celery worker --loglevel=info
```
