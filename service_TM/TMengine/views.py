from TMengine.engine_trainer import update_model
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import LdaModel
import urllib3
import json


class LdaModelViewSet(viewsets.ViewSet):
    queryset = LdaModel.objects.all()

    @staticmethod
    def list(request):
        return Response(data={":)"})

    @staticmethod
    def create(request):
        try:

            # Get news to update LDA model
            http = urllib3.PoolManager()
            request = http.request('GET', 'http://corpus_data:4000/api/documents/')
            data_request = json.loads(request.data.decode('utf-8'))
            corpus = []
            for document in data_request['documents']['records']:
                corpus.append(document['clean_text'])
            # Trigger async task to update LDA model
            update_model(corpus)
            response_message = {"Model update start!"}
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
        return Response(data={":)"})

    @staticmethod
    def partial_update(request, pk=None):
        return Response(data={":)"})

    @staticmethod
    def destroy(request, pk=None):
        return Response(data={":)"})



