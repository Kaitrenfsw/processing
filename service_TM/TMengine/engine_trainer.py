import os
import gensim
import datetime
import collections
import urllib3
import json
import random
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

    print(news_tokenized)
    # Creating the term dictionary of our courpus, where every unique term is assigned an index
    dictionary = corpora.Dictionary(news_tokenized)
    print(dictionary)
    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in news_tokenized]
    print(doc_term_matrix)
    # Getting latest (in_use) model
    dirname = os.path.dirname(__file__)
    latest_model = LdaModel.objects.get(in_use=True)
    latest_filepath = os.path.join(dirname, 'lda_model/' + latest_model.filename)

    # Create object for LDA model
    lda_multicore = gensim.models.ldamulticore.LdaMulticore
    # Loading latest model in use
    lda_instance = lda_multicore.load(latest_filepath)
    # Updating model
    print("Start update LDA Model" + latest_model.filename)
    lda_instance.update(corpus=doc_term_matrix)
    # Save new model instance
    date_now = datetime.datetime.now().strftime("%y_%m_%d_%H_%M_%S")
    new_filename = "lda_" + date_now + ".model"
    new_file_path = os.path.join(dirname, 'lda_model/' + new_filename)
    lda_instance.save(new_file_path)
    print("Finish update LDA Model, New model created:" + new_filename)

    # Save new data of model in DB and change flag of newest in old model
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
        topic_dict["name"] = "New Topic"
        topic_dict["coherence"] = str(round(random.random(), 2))
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
    topics = model.show_topics(num_topics=-1, num_words=20, formatted=False)

    # transform to json format
    topics_list = []
    for topic in topics:
        topic_dict = dict()
        topic_dict["topic_number"] = topic[0]
        topic_dict["coherence"] = str(round(random.random(), 2))
        topic_dict["lda_model_id"] = 1
        topic_dict["keyword_topic"] = []
        for keyword in topic[1]:
            keyword_dict = dict()
            keyword_dict["name"] = keyword[0]
            keyword_dict["weight"] = str(round(keyword[1], 10))
            topic_dict["keyword_topic"].append(keyword_dict)
        topics_list.append(topic_dict)
    json_data = json.dumps(topics_list)

    # HTTP pool request
    http = urllib3.PoolManager()
    # Send new model info and topics to business rules service
    http.request('POST', 'http://business-rules:8001/topic/', body=json_data,
                 headers={'Content-Type': 'application/json'})


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
        classifications = lda_instance.get_document_topics(bow=doc_term_matrix, minimum_probability=0.05)

        # Formatting new info JSON object
        document['topics'] = []
        document['cat_date'] = datetime.datetime.now().strftime("%d/%m/%Y")
        document['text'] = document.pop('clean_text')
        document.pop('id')
        document.pop('updated_at')
        document.pop('created_at')


        # Create array with internal ids from topics and weight associated
        for classification in classifications[0]:
            document['topics'].append({'id': classification[0],
                                       'weight': str(round(classification[1], 10))})

        # HTTP pool request
        http = urllib3.PoolManager()
        # GET Request to business_rules with topics ids
        request_1 = http.request('GET', 'http://business-rules:8001/ldamodelTopics/1',
                                 headers={'Content-Type': 'application/json'})
        topics_data = json.loads(request_1.data.decode('utf-8'))


        date = datetime.datetime.strptime(document['published'], "%d/%m/%Y")
        date_reformatted = date.date().strftime("%Y-%m-%d")

        request_2 = http.request('GET', 'http://business-rules:8001/dateConversion/'
                                 + date_reformatted,
                                 headers={'Content-Type': 'application/json'})

        week_code = json.loads(request_2.data.decode('utf-8'))
        document['int_published'] = week_code[0]['week']


        # Replace topic internal number with id from business_rules service
        aux_document = []
        for topic in document['topics']:
            for topic_data in topics_data[0]:
                if topic_data['topic_number'] == topic['id']:
                    aux_document.append({"id": topic_data['id'], "weight": topic['weight']})

        # Request body formatting and encoding
        document['topics'] = aux_document
        news_classified.append(document)
        new_classified = dict()
        new_classified['document'] = news_classified[0]
        print(new_classified)
        encoded_data = json.dumps(new_classified).encode('utf-8')

        # POST Request to categorized-data service
        request_3 = http.request('POST', 'http://categorized_data:4000/api/documents/',
                                 body=encoded_data,
                                 headers={'Content-Type': 'application/json'})
        return request_3.status


def topic_relation():

    # Get latest lda model saved
    dirname = os.path.dirname(__file__)
    latest_model = LdaModel.objects.get(in_use=True)
    latest_filepath = os.path.join(dirname, 'lda_model/' + latest_model.filename)

    # Create object for LDA model
    lda_multicore = gensim.models.ldamulticore.LdaMulticore
    # Loading latest model in use
    lda_instance_1 = lda_multicore.load(latest_filepath)
    lda_instance_2 = lda_multicore.load(latest_filepath)

    # (row -> self.num_topics, col -> other.num_topics)
    topic_diff_matrix, annotation = lda_instance_1.diff(lda_instance_2)

    # Based in topic_diff matrix calculate differences between all topics in the same model
    matrix_shape = topic_diff_matrix.shape
    relations = []
    relation_dict = {}
    for row in range(0, matrix_shape[0]):
        keywords_1 = lda_instance_1.show_topic(topicid=row, topn=20)
        for col in range(0, matrix_shape[1]):
            relation_dict["topic_1"] = row
            relation_dict["topic_2"] = col
            relation_dict["distance"] = round(topic_diff_matrix[row][col], 10)

            keywords_2 = lda_instance_2.show_topic(topicid=col, topn=20)
            keywords = []
            for keyword_1 in keywords_1:
                for keyword_2 in keywords_2:
                    if keyword_1[0] == keyword_2[0]:
                        keywords.append(keyword_1[0])
            relation_dict["keywords_match"] = keywords
            relations.append(relation_dict)
            relation_dict = {}

    request_body = dict()
    request_body["lda_filename"] = latest_model.filename
    request_body["lda_model_id"] = 1
    request_body["relations"] = relations
    print(request_body)
    encoded_data = json.dumps(request_body).encode('utf-8')

    # HTTP pool request
    http = urllib3.PoolManager()
    # GET Request to business_rules with topics ids
    request = http.request('POST', 'http://business-rules:8001/topicComparison/',
                           body=encoded_data,
                           headers={'Content-Type': 'application/json'})






