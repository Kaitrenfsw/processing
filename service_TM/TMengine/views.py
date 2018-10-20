from TMengine.engine_trainer import update_model, topic_relation
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import LdaModel, TrainingStatus
from .serializers import TrainingStatusSerializer
import requests


class LdaModelViewSet(viewsets.ViewSet):
    queryset = LdaModel.objects.all()

    @staticmethod
    def list(request):
        return Response(data={":)"})

    @staticmethod
    def create(request):
        training_status = TrainingStatus.objects.get(pk=1)
        training_status.is_training = True
        training_status.save()
        try:
            # Request to corpus_data service
            url = 'http://corpus_data:4000/api/documents/'
            data_request = requests.get(url)

            # Get news to update LDA model
            documents = data_request.json()
            corpus = []
            for document in documents['documents']['records']:
                corpus.append(document['clean_text'])

            print(training_status.is_training)
            # Trigger async task to update LDA model
            update_model(corpus)
            training_status.is_training = False
            training_status.save()

            response_message = {"Model update finished!"}
            status_message = status.HTTP_200_OK
        except Exception as e:

            training_status.is_training = False
            training_status.save()

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


class TrainingStatusViewSet(viewsets.ViewSet):
    queryset = TrainingStatus.objects.all()

    @staticmethod
    def list(request):
        try:
            training_status = TrainingStatus.objects.get(pk=1)
            training_status_serialized = TrainingStatusSerializer(training_status).data
            response_message = training_status_serialized
            status_message = status.HTTP_200_OK
        except Exception as e:
            response_message = {e}
            status_message = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response(data=response_message, status=status_message)

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


class TopicRelationViewSet(viewsets.ViewSet):
    queryset = LdaModel.objects.all()

    @staticmethod
    def list(request):
        try:
            topic_relation()
            status_message = status.HTTP_200_OK
            response_message = {""}
        except Exception as e:
            response_message = {e}
            status_message = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response(data=response_message, status=status_message)

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
