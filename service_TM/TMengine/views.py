from new.models import New
from topic.serializers import TopicSerializer, KeywordSerializer
from TMengine.engine_trainer import update_or_create_newest_model
from rest_framework import viewsets, status
from rest_framework.response import Response


class LdaModelViewSet(viewsets.ViewSet):

    @staticmethod
    def list(request):
        return Response(data={":)"})

    @staticmethod
    def create(request):
        data = request.data
        try:
            news = list(New.objects.all().values_list('full_text', flat=True))
            new_name = update_or_create_newest_model(data["action"], news)
            response_message = {"New Model created successfully!, new filename: " + new_name}
            status_message = status.HTTP_200_OK
        except Exception as e:
            response_message = {e}
            status_message = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response(data=response_message,
                        status=status_message)

    @staticmethod
    def retrieve(request, pk=None):
        return Response(data={":)"})

    @staticmethod
    def update(request, pk=None):
        data = request.data
        try:
            news = list(New.objects.all().values_list('full_text', flat=True))
            new_name = update_or_create_newest_model(data["action"], news)
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
    'put': 'update',
    'post': 'create',
})
