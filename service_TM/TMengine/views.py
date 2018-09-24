from TMengine.engine_trainer import update_model
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import LdaModel
import requests
import json


class LdaModelViewSet(viewsets.ViewSet):
    queryset = LdaModel.objects.all()

    @staticmethod
    def list(request):
        return Response(data={":)"})

    @staticmethod
    def create(request):
        try:
            # Request to corpus_data service
            url = 'http://corpus_data:4000/api/documents/'
            data_request = requests.get(url)

            # Get news to update LDA model
            documents = data_request.json()
            corpus = []
            for document in documents['documents']['records']:
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



