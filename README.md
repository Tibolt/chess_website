# Chess website project

# How to launch
## Postgres database in docker
``` bash
docker create volume pgdata
docker run --name postgresdb -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpass
docker exec -it postgresdb bash
```

##Connect to psql and create table
``` bash
psql -h 127.0.0.1 -p 5432 -U postgres
CREATE DATABASE website;
```

##Download python requirments and run dev server
``` bash
pip install -r requirments.txt
python manage.py migrate
python manage.py runserver 8888
```
