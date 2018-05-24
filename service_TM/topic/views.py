from .models import Topic, Keyword, TopicUser, LdaModel
from .serializers import KeywordSerializer, TopicKeywordSerializer
from TMengine.engine_trainer import get_topics
from rest_framework import viewsets, status
from rest_framework.response import Response


class TopicViewSet(viewsets.ViewSet):

    @staticmethod
    def list(request):
        topics = Topic.objects.all()
        response_json = []
        response_status = ""
        try:
            for topic in topics:
                serialized_topic = TopicKeywordSerializer(topic).data
                response_json.append(serialized_topic)
                response_status = status.HTTP_200_OK
        except Exception as e:
            response_json = {"Exception raised": e}
            response_status = status.HTTP_404_NOT_FOUND

        return Response(data=response_json, status=response_status)

    @staticmethod
    def create(request):
        if ('topic_number' and 'corpus_number' and 'topic_name') in request.data:
            try:
                new_topic_data = request.data
                new_topic = Topic(topic_number=new_topic_data['topic_number'],
                                  corpus_number=new_topic_data['corpus_number'],
                                  name=new_topic_data['topic_name'])
                new_topic.save()
                response_message = {"New Topic added successfully"}
                response_status = status.HTTP_200_OK
            except Exception as e:
                response_message = {"Exception raised": e}
                response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            response_message = {"Bad Request, check sent parameters"}
            response_status = status.HTTP_400_BAD_REQUEST

        return Response(data=response_message, status=response_status)

    @staticmethod
    def retrieve(request, pk=None):
        return Response(data={":)"})

    @staticmethod
    def update(request, pk=None):
        new_topics = get_topics()
        for topic in new_topics:
            ldamodel_instance = LdaModel.objects.get(filename=topic['lda_model'])
            topic_instance = Topic(topic_number=topic['topic_number'],
                                   lda_model=ldamodel_instance)
            topic_instance.save()
            for keyword in topic["keywords"]:
                keyword_instance = Keyword(name=keyword['name'],
                                           weight=round(keyword['weight'], 2),
                                           topic_id=topic_instance)
                keyword_instance.save()
        return Response(data=new_topics)

    @staticmethod
    def partial_update(request, pk=None):
        return Response(data={":)"})

    @staticmethod
    def destroy(request, pk=None):
        return Response(data={":)"})


topic_list = TopicViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'put': 'update',
})


class KeywordViewSet(viewsets.ViewSet):

    @staticmethod
    def list(request):
        try:
            response_json = KeywordSerializer(Keyword.objects.all(), many=True).data
            response_status = status.HTTP_200_OK
        except Exception as e:
            response_json = {"Exception raised": e}
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(data=response_json, status=response_status)

    @staticmethod
    def create(request):
        return Response(data={":)"})

    @staticmethod
    def retrieve(request, pk=None):
        return Response(data={":)"})

    @staticmethod
    def update(request, pk=None):
        return Response(data={":)"})

    @staticmethod
    def partial_update(request, pk=None):
        return Response(data={":)"})

    @staticmethod
    def destroy(request, pk=None):
        return Response(data={":)"})


keyword_list = KeywordViewSet.as_view({
    'get': 'list',
})


class TopicUserViewSet(viewsets.ViewSet):

    @staticmethod
    def list(request):
        if 'user_id' in request.data:
            try:
                user_info = request.data
                user_topics = TopicUser.objects.filter(user_id=user_info["user_id"]).values_list('id')
                topics = Topic.objects.filter(id__in=user_topics)
                response_message = []
                for topic in topics:
                    serialized_topic = TopicKeywordSerializer(topic).data
                    response_message.append(serialized_topic)
                response_status = status.HTTP_200_OK
            except Exception as e:
                response_message = {"Exception raised" : e}
                response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            response_message = {"Bad Request, check sent parameters"}
            response_status = status.HTTP_400_BAD_REQUEST

        return Response(data=response_message, status=response_status)

    @staticmethod
    def create(request):
        return Response(data={":)"})

    @staticmethod
    def retrieve(request, pk=None):
        return Response(data={":)"})

    @staticmethod
    def update(request, pk=None):
        if ('topic_id' and 'user_topics_id') in request.data:
            try:
                data = request.data
                older_topics = TopicUser.objects.filter(user_id=1).values_list('topic_id', flat=True)
                updated_topics = data["user_topics_id"]

                # adding new topics that didn't exist
                for new_topic_id in updated_topics:
                    if new_topic_id not in older_topics:
                        topic_instance = Topic.objects.get(id=new_topic_id)
                        topic = TopicUser(user_id=data['user_id'], topic_id=topic_instance)
                        topic.save()
                # deleting topics
                for old_topic_id in older_topics:
                    if old_topic_id not in updated_topics:
                        topic_user_instance = TopicUser.objects.get(id=old_topic_id)
                        topic_user_instance.delete()
                response_message = {"Topics updated successfully!"}
                response_status = status.HTTP_200_OK
            except Exception as e:
                response_message = {"Exception raised": e}
                response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            response_message = {"Bad Request, check sent parameters"}
            response_status = status.HTTP_400_BAD_REQUEST

        return Response(data=response_message, status=response_status)

    @staticmethod
    def partial_update(request, pk=None):
        return Response(data={":)"})

    @staticmethod
    def destroy(request, pk=None):
        return Response(data={":)"})


topicUser_list = TopicUserViewSet.as_view({
    'post': 'list',
    'put': 'update',
})
