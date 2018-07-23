# Topics administration API
Database: Postgres  9.5.12>=

## How to Run?

## Running with Docker:

``` $ docker-compose up```

Run fixture in container to load data:

``` docker-compose exec procesamiento python3 service_TM/manage.py loaddata service_TM/fixture.json```


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


#API Endpoints:

##### Topic: [http://127.0.0.1:8000/topic/](http://127.0.0.1:8000/topic/)

- methods allowed: GET
- Request: empty
- Response: All topics available
- Response format:
``` [
    {
        "id": 1,
        "topic_number": 0,
        "lda_model": 1,
        "name": null,
        "keyword_topic": [
            {
                "id": 1,
                "name": "ad",
                "weight": 0.00999999977648258
            },
            {
                "id": 2,
                "name": "food",
                "weight": 0.00999999977648258
            },
            {
                "id": 3,
                "name": "ads",
                "weight": 0.00999999977648258
            },
            ...
        ]
    },
    {
        "id": 2,
        "topic_number": 1,
        "lda_model": 1,
        "name": null,
        "keyword_topic": [
            {
                "id": 6,
                "name": "say",
                "weight": 0.0299999993294477
            },
            {
                "id": 7,
                "name": "us",
                "weight": 0.00999999977648258
            },
            ...
        ]
    },
    ...
    
]
``` 
- methods allowed: POST
- Request: 
``` 
{
	"topic_number": 1,
	"lda_model_filename": "lda_01_20000.model",
	"topic_name": "topic1"
}
```
- Response: Status message
- Response format:
```
- HTTP_200_OK: {"New Topic added successfully"}
- HTTP_500_INTERNAL_SERVER_ERROR: {<specific exception>}
- HTTP_400_BAD_REQUEST: {"Bad Request, check sent parameters"}
```

- methods allowed: PUT
- Request: empty
- Action: save in database topics and keywords for LDA model marked as newest in database.
- Response: List of data saved in database
- Response format: 
``` 
[
    {
        "topic_number": 0,
        "keywords": [
            {
                "weight": 0.009595467709004879,
                "name": "ad"
            },
            {
                "weight": 0.008851521648466587,
                "name": "food"
            },
            {
                "weight": 0.00771958427503705,
                "name": "ads"
            },
            {
                "weight": 0.006286182440817356,
                "name": "advertise"
            },
            {
                "weight": 0.005742626264691353,
                "name": "pope"
            }
        ],
        "lda_model": "lda_03_22292_20_.model"
    },
    ...
]
``` 

##### Keyword: [http://127.0.0.1:8000/keyword/](http://127.0.0.1:8000/keyword/)

- methods allowed: GET
- Request: empty
- Response: All keywords available
- Response format:
``` [
    {
        "id": 1,
        "name": "django",
        "weight": 0.02,
        "topic_id": 1
    },
    {
        "id": 2,
        "name": "framework",
        "weight": 0.22,
        "topic_id": 1
    },
    ...
]
```
##### TopicUser: [http://127.0.0.1:8000/topicUser/](http://127.0.0.1:8000/topicUser/)

- methods allowed: POST
- Request: 
``` 
{
	"user_id": 12
}
```
- Response: All topics and keywords selected for a certain User
- Response format:
``` [
    {
        "id": 1,
        "topic_number": 0,
        "lda_model": 1,
        "name": null,
        "keyword_topic": [
            {
                "id": 1,
                "name": "ad",
                "weight": 0.00999999977648258
            },
            {
                "id": 2,
                "name": "food",
                "weight": 0.00999999977648258
            },
            ...
        ]
    },
    ...
]
```

- methods allowed: PUT
- action: update topics related to certain user
- Request: 
``` 
{
	"user_id": 12
	"user_topics_id": [1, 18]
}
```
- Response: Status message
- Response format:
```
- HTTP_200_OK: {"Topics updated successfully"}
- HTTP_500_INTERNAL_SERVER_ERROR: {<specific exception>}
- HTTP_400_BAD_REQUEST: {"Bad Request, check sent parameters"}
```


### LdaModel

- methods allowed: PUT
- action: update LDA model, save filename, change status to newest and save new topics
- Request: Empty
```
{}
```
- Response: Status message
- Response format:
```
- HTTP_200_OK: {"Model updated successfully!, new filename: " + new_name}}
- HTTP_500_INTERNAL_SERVER_ERROR: {<specific exception>}
```

- methods allowed: POST
- action: Classify a new into different topics
- Request: 
```

{
    "date": "<date>",
    "doc_count": "<number of documents>",
    "documents": [
        {
            "title": "<document title>",
            "url": "<document url>",
            "site": "<site url>",
            "site_name": "<site name>",
            "published": "<date>",
            "main_image": "<image url>",
            "text": "Lorem ipsum..."
        }
    ]
} 
```
Response format:
```
{
    "id_model": 1,
    "model_used": "LDA_100_topics_28_05_2018_passes_20.model",
    "classification": [
        [
            81,
            0.6700000166893005
        ],...
    ]
}
```