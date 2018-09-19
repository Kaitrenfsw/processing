from new.models import New
from TMengine.engine_trainer import update_model
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import LdaModel


class LdaModelViewSet(viewsets.ViewSet):
    queryset = LdaModel.objects.all()

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
        try:
            # Get news to update LDA model
            news = list(New.objects.all().values_list('text', flat=True))
            # Trigger async task to update LDA model
            update_model(news)
            response_message = {"Model update start!"}
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



