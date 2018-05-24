from topic.models import Topic, Keyword
from topic.serializers import TopicSerializer, KeywordSerializer
from rest_framework import viewsets
from rest_framework.response import Response


class LdaModelViewSet(viewsets.ViewSet):

    @staticmethod
    def list(request):
        return Response(data={":)"})

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


lda_model_list = LdaModelViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
