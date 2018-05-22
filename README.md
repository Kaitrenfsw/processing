# Topics administration API

## How to Run?

### Linux/MacOS

Install a virtualenv with python3 more info [here](https://rukbottoland.com/blog/tutorial-de-python-virtualenv/)


Run the virtualenv:

``` $ source venv/bin/activate```

Install requirements.txt:
``` $ pip install -r requirements.txt ```

Run Django API from service_TM folder:

``` $ python manage.py runserver ```


API Endpoints:

Topic: [http://127.0.0.1:8000/topic/](http://127.0.0.1:8000/topic/)

- methods allowed: GET
- Request: empty
- Response: All topics available
- Response format:
``` [
    {
        "topic": {
            "id": 1,
            "topic_number": 1,
            "corpus_number": 1,
            "name": "Python",
            "keywords": [
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
        }
    },
    {
        "topic": {
            "id": 2,
            "topic_number": 2,
            "corpus_number": 1,
            "name": "Ruby",
            "keywords": []
        }
    }
    ...
]
``` 

Keyword: [http://127.0.0.1:8000/keyword/](http://127.0.0.1:8000/keyword/)

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
TopicUser: [http://127.0.0.1:8000/topicUser/](http://127.0.0.1:8000/topicUser/)

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
        "topic": {
            "id": 1,
            "user_id": 1,
            "topic_id": 1,
            "keywords": [
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
                {
                    "id": 3,
                    "name": "language",
                    "weight": 0.29,
                    "topic_id": 1
                },
                   ...
            ]
        }
    }
]
```
