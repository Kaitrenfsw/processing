from topic.models import Topic, Keyword, TopicUser
from topic.serializers import TopicSerializer, KeywordSerializer, TopicUserSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response


class TopicViewSet(viewsets.ViewSet):

    @staticmethod
    def list(request):
        topics = Topic.objects.all()
        response_array = []
        for topic in topics:
            dic_of_topics = {}
            keywords = Keyword.objects.filter(topic_id=topic.pk)
            dic_of_topics['topic'] = TopicSerializer(topic).data
            dic_of_topics['topic']['keywords'] = KeywordSerializer(keywords, many=True).data
            response_array.append(dic_of_topics)
        return Response(data=response_array, status=status.HTTP_200_OK)

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


topic_list = TopicViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'put': 'update',
})


class KeywordViewSet(viewsets.ViewSet):

    @staticmethod
    def list(request):
        queryset = KeywordSerializer(Keyword.objects.all(), many=True).data
        return Response(data=queryset, status=status.HTTP_200_OK)

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


keyword_list = TopicViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'put': 'update',
})


class TopicUserViewSet(viewsets.ViewSet):

    @staticmethod
    def list(request):
        usertopics = TopicUser.objects.filter(user_id=1)
        response_array = []
        for topic in usertopics:
            dic_of_topics = {}
            keywords = Keyword.objects.filter(topic_id=topic.pk)
            dic_of_topics['topic'] = TopicUserSerializer(topic).data
            dic_of_topics['topic']['keywords'] = KeywordSerializer(keywords, many=True).data
            response_array.append(dic_of_topics)

        return Response(data=response_array, status=status.HTTP_200_OK)

    @staticmethod
    def create(request):
        return Response(data={":)"})

    @staticmethod
    def retrieve(request, pk=None):
        return Response(data={":)"})

    @staticmethod
    def update(request, pk=None):
        return Response(data={":123)"})

    @staticmethod
    def partial_update(request, pk=None):
        if 'id' in request.data:
            print(":()")
        else:
            print("chan!")
        return Response(data={":)456"})

    @staticmethod
    def destroy(request, pk=None):
        return Response(data={":)"})


topicUser_list = TopicUserViewSet.as_view({
    'post': 'create',
    'put': 'update',
    'patch': 'partial_update',
    'view': 'list',
})
