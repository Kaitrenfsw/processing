import os
import gensim
import datetime
import collections
import urllib3
import json
import requests
from gensim import corpora
from .models import LdaModel
from .serializers import LdaModelSerializer
from celery import shared_task


# @shared_task
def update_model(data_array):

    # HTTP pool request
    http = urllib3.PoolManager()

    news_tokenized = []
    for new in data_array:
        news_tokenized.append(new.split())

    # Creating the term dictionary of our courpus, where every unique term is assigned an index
    dictionary = corpora.Dictionary(news_tokenized)

    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in news_tokenized]

    # Getting latest (in_use) model
    dirname = os.path.dirname(__file__)
    latest_model = LdaModel.objects.get(in_use=True)
    latest_filepath = os.path.join(dirname, 'lda_model/' + latest_model.filename)

    # Create object for LDA model
    lda_multicore = gensim.models.ldamulticore.LdaMulticore
    # Loading latest model in use
    lda_instance = lda_multicore.load(latest_filepath)
    # Updating model
    print("start update")
    lda_instance.update(corpus=doc_term_matrix)
    print("finish update")
    # Save new model instance
    date_now = datetime.datetime.now().strftime("%y_%m_%d")
    new_filename = "lda_" + date_now + ".model"
    new_file_path = os.path.join(dirname, 'lda_model/' + new_filename)
    lda_instance.save(new_file_path)

    # Save new data of model in DB and change flag of newest
    latest_model.newest = False
    latest_model.save()
    updated_model = LdaModel(filename=new_filename)
    updated_model.save()

    # Compare distribution difference from each topic from latest and new model
    old_model = lda_multicore.load(latest_filepath)
    new_model = lda_multicore.load(new_file_path)
    # (row -> self.num_topics, col -> other.num_topics)
    topic_diff_matrix, annotation = old_model.diff(new_model)

    # Based in topic_diff matrix, search for topics with a distribution difference
    # higher than 0.75
    new_topics = []
    matrix_shape = topic_diff_matrix.shape
    for row in range(0, matrix_shape[0]):
        for col in range(0, matrix_shape[1]):
            if topic_diff_matrix[row][col] > 0.75:
                new_topics.append(col)
    # Dict key: topic number, value: frequency of condition passed across all topics
    new_topics_frequency = collections.Counter(new_topics)
    topics_to_add = []
    # Select new topics based in frequency of high distribution difference within a threshold
    threshold = 25
    for topic_number, frequency in new_topics_frequency.items():
        if frequency > threshold:
            topics_to_add.append(topic_number)

    # Search for new topic an create json response
    topics_list = []
    for new_topic_id in topics_to_add:
        topic_keywords = new_model.show_topic(topicid=new_topic_id, topn=20)
        topic_dict = dict()
        topic_dict["lda_model_id"] = updated_model.pk
        topic_dict["topic_number"] = new_topic_id
        topic_dict["keyword_topic"] = []
        for keyword, weight in topic_keywords:
            keyword_dict = dict()
            keyword_dict["name"] = keyword
            keyword_dict["weight"] = str(round(weight, 10))
            topic_dict["keyword_topic"].append(keyword_dict)
        topics_list.append(topic_dict)
    json_data = json.dumps(topics_list)

    # Send new model info and topics to business rules service
    http.request('POST', 'http://business-rules:8001/topic/', body=json_data,
                 headers={'Content-Type': 'application/json'})


def get_topics():
    dirname = os.path.dirname(__file__)
    file_instance = LdaModel.objects.get(newest=True).filename
    filename = os.path.join(dirname, 'lda_model/' + file_instance)

    # Creating the object for LDA model
    lda_multicore = gensim.models.ldamulticore.LdaMulticore

    # Loading actual LDA model
    model = lda_multicore.load(filename)

    # Getting topics from model
    topics = model.show_topics(num_topics=-1, num_words=10, formatted=False)

    # transform to json format
    topics_list = []
    for topic in topics:
        topic_dict = dict()
        topic_dict["topic_number"] = topic[0]
        topic_dict["lda_model"] = file_instance
        topic_dict["keyword_topic"] = []
        for keyword in topic[1]:
            keyword_dict = dict()
            keyword_dict["name"] = keyword[0]
            keyword_dict["weight"] = keyword[1]
            topic_dict["keyword_topic"].append(keyword_dict)
        topics_list.append(topic_dict)
    json_data = json.dumps(topics_list)
    return json_data


def classify_new(documents):

    # Getting latest (newest) model
    dirname = os.path.dirname(__file__)
    latest_model = LdaModel.objects.get(in_use=True)
    filename = os.path.join(dirname, 'lda_model/' + latest_model.filename)

    # Creating the object for LDA model and getting the classification
    lda_multicore = gensim.models.ldamulticore.LdaMulticore
    lda_instance = lda_multicore.load(filename)

    news_classified = []
    for document in documents:
        new_tokenized = [document['clean_text'].split()]
        # Creating the term dictionary of our courpus, where every unique term is assigned an index
        dictionary = corpora.Dictionary(new_tokenized)
        # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
        doc_term_matrix = [dictionary.doc2bow(doc) for doc in new_tokenized]
        # Classification format [(<topic number>, <percentage>), ...]
        classifications = lda_instance.get_document_topics(bow=doc_term_matrix, minimum_probability=0.15)

        # Formatting new info JSON object
        document['topics'] = []
        document['cat_date'] = datetime.datetime.now().strftime("%d-%m-%Y")
        document['text'] = document.pop('clean_text')
        document.pop('id')
        document.pop('updated_at')
        document.pop('created_at')

        # Create array with internal ids from topics and weight associated
        for classification in classifications[0]:
            document['topics'].append({'id': classification[0],
                                       'weight': classification[1]})

        # HTTP pool request
        http = urllib3.PoolManager()
        # GET Request to business_rules with topics ids
        request = http.request('GET', 'http://business-rules:8001/ldamodelTopics/'
                               + str(latest_model.pk),
                               headers={'Content-Type': 'application/json'})
        topics_data = json.loads(request.data.decode('utf-8'))

        # Replace topic internal number with id from business_rules service
        for topic_data in topics_data[0]:
            for topic in document['topics']:
                if topic_data['topic_number'] == topic['id']:
                    topic['id'] = topic_data['id']

        # Request body formatting and encoding
        news_classified.append(document)
        new_classified = dict()
        new_classified['document'] = news_classified[0]
        encoded_data = json.dumps(new_classified).encode('utf-8')

        # POST Request to categorized-data service
        request = http.request('POST', 'http://categorized_data:4000/api/documents/',
                               body=encoded_data,
                               headers={'Content-Type': 'application/json'})
        print(request.status)
        return request.status




