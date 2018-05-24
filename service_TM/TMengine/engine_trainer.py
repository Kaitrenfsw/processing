import os
import glob
import errno
import gensim
from gensim import corpora
from .models import LdaModel



def modelTrainer(action, new_docs):
    # Currently the trainer is fed reading a set of files in .txt format
    # Change path directory before run the trainer
    ####################################################################################################
    path = '/home/simon/Desktop/tech_news/corpus/*.txt'
    files = glob.glob(path)
    news = []
    for file_path in files:
        try:
            with open(file_path, mode='r') as new:
                news.append(new.read())
        except IOError as exc:
            if exc.errno != errno.EISDIR:  # Do not fail if a directory is found, just ignore it.
                raise

    news_tokenized = []
    for new in news:
        news_tokenized.append(new.split())
    number_documents = len(news_tokenized)
    ####################################################################################################

    # Creating the term dictionary of our courpus, where every unique term is assigned an index
    dictionary = corpora.Dictionary(news_tokenized)

    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in news_tokenized]

    # Creating the object for LDA model using gensim library
    lda_multicore = gensim.models.ldamulticore.LdaMulticore
    num_topics = 20
    workers = 3

    if action == 'update':
        latest_model = LdaModel.objects.get(newest=True)
        model_path = "lda_model/"
        lda_instance = lda_multicore.load(model_path + latest_model.name)
        #lda_instance.update(corpus=doc_term_matrix)
        #filename = "lda_model/lda_" + str(latest_model.pk + 1) + "_" + str(number_documents) + "_" + str(num_topics) + "_.model"
        #lda_instance.save(filename)
        print(lda_instance.print_topics(num_topics=20, num_words=5))
    if action == 'create':
        # Running and Training LDA model on the document term matrix.
        lda_instance = lda_multicore(corpus=doc_term_matrix, num_topics=num_topics,
                                     id2word=dictionary, passes=50, workers=workers)
        # Filename for LDA model
        number = LdaModel.objects.get(newest=True).pk + 1
        filename = "lda_model/lda_" + str(number) + "_" + str(number_documents) + "_" + str(num_topics) + "_.model"
        lda_instance.save(filename)


def get_topics():
    dirname = os.path.dirname(__file__)
    file_instance = LdaModel.objects.get(newest=True).filename
    filename = os.path.join(dirname, 'lda_model/' + file_instance)

    # Creating the object for LDA model
    lda_multicore = gensim.models.ldamulticore.LdaMulticore

    # Loading actual LDA model
    model = lda_multicore.load(filename)

    # Getting topics from model
    topics = model.show_topics(num_topics=20, num_words=5, formatted=False)

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



