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

Now you can access the app in localhost:5000

<br/>
<br/>


**Celery scheduler**

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
<br/>
<br/>

**API**<br/>
Register user : 
```
URL : localhost:5000/api/v1/users
METHOD : Post
BODY : 
{ email : string, password : string}
```

Login : 
```
URL : localhost:5000/api/v1/login
METHOD : Post
BODY : 
{ email : string, password : string}
```

List file : 
```
URL : localhost:5000/api/v1/files
METHOD : Get
```


Upload file : 
```
URL : localhost:5000/api/v1/files
METHOD : Post
CONTENT-TYPE: multipart/form-data
BODY: 
- file 
```
<br/>
<br/>

**NOTES**

- I don't know wether the flask and the celery should be seprated application or could be in one, I set it up in one application
- I am new about celery, and still learning how to deploy it in docker properly
- Migrating database should be done manually for now
