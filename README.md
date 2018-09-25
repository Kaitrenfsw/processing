# Topics administration API
Database: Postgres  9.5.12>=

## How to Run?

## Running with Docker:

``` $ docker-compose up```

Run fixture in container to load data:

``` docker-compose exec processing python3 service_TM/manage.py loaddata service_TM/fixture.json```


### Linux/MacOS

Install a virtualenv with python3 more info [here](https://rukbottoland.com/blog/tutorial-de-python-virtualenv/)


Run the virtualenv:

``` $ source venv/bin/activate```

Install requirements.txt:

``` $ pip install -r requirements.txt ```

Run Migrations and fixture from service_TM folder:

``` python manage.py makemigrations ```

``` python manage.py migrate ```

```python manage.py loaddata fixture.json```

Run Django API from service_TM folder:

``` $ python manage.py runserver ```


# API Endpoints use via BFF:

##### Topic: [http://127.0.0.1:8000/ldamodel/](http://127.0.0.1:8000/topic/)

- methods allowed: POST
- Request: empty
- Response: empty
- Response format:
``` 
    ["Model update start!"] STATUS CODE 200 
    [{e}] STATUS CODE 500
```

##### Topic: [http://127.0.0.1:8000/trainingStatus/](http://127.0.0.1:8000/topic/)

- methods allowed: GET
- Request: empty
- Response: empty
- Response format:
``` 
    {"id":1,"is_training":false} STATUS CODE 200 
    [{e}] STATUS CODE 500
```

