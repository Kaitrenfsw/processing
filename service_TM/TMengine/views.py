from topic.models import Topic, Keyword
from topic.serializers import TopicSerializer, KeywordSerializer
from TMengine.engine_trainer import update_newest_model, document_classifier
from rest_framework import viewsets, status
from rest_framework.response import Response


class LdaModelViewSet(viewsets.ViewSet):

    @staticmethod
    def list(request):
        return Response(data={":)"})

    @staticmethod
    def create(request):
        data = request.data
        response_message = document_classifier(data["text"])
        return Response(data=response_message)

    @staticmethod
    def retrieve(request, pk=None):
        return Response(data={":)"})

    @staticmethod
    def update(request, pk=None):
        data = request.data
        try:
            new_name = update_newest_model(data)
            response_message = {"Model updated successfully!, new filename: " + new_name}
            status_message = status.HTTP_200_OK
        except Exception as e:
            response_message = {e}
            status_message = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response(data=response_message,
                        status=status_message)

    @staticmethod
    def partial_update(request, pk=None):
        return Response(data={":)"})

    @staticmethod
    def destroy(request, pk=None):
        return Response(data={":)"})


lda_model_list = LdaModelViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'put': 'update',
})


