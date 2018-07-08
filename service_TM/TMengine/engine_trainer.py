import os
import gensim
from gensim import corpora
from .models import LdaModel


def update_or_create_newest_model(action, data_array):

    news_tokenized = []
    for new in data_array:
        news_tokenized.append(new.split())

    # Creating the term dictionary of our courpus, where every unique term is assigned an index
    dictionary = corpora.Dictionary(news_tokenized)

    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in news_tokenized]

    # Getting latest (newest) model
    dirname = os.path.dirname(__file__)
    latest_model = LdaModel.objects.get(newest=True)
    filename = os.path.join(dirname, 'lda_model/' + latest_model.filename)
    # Creating the object for LDA model
    lda_multicore = gensim.models.ldamulticore.LdaMulticore

    if action == "update":
        lda_instance = lda_multicore.load(filename)
        lda_instance.update(corpus=doc_term_matrix)
    if action == "create":
        num_topics = 100
        workers = 3
        passes = 10
        lda_instance = lda_multicore(corpus=doc_term_matrix,
                                     num_topics=num_topics,
                                     id2word=dictionary,
                                     workers=workers,
                                     passes=passes)

    new_filename = "lda_" + str(latest_model.pk) + ".model"
    new_file_path = os.path.join(dirname, 'lda_model/' + new_filename)
    lda_instance.save(new_file_path)
    latest_model.newest = False
    latest_model.save()
    updated_model = LdaModel(filename=new_filename)
    updated_model.save()

    return new_filename


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
        topic_dict["keywords"] = []
        for keyword in topic[1]:
            keyword_dict = dict()
            keyword_dict["name"] = keyword[0]
            keyword_dict["weight"] = keyword[1]
            topic_dict["keywords"].append(keyword_dict)
        topics_list.append(topic_dict)

    return topics_list


