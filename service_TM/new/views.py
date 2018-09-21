from rest_framework import viewsets, status
from rest_framework.response import Response
from TMengine.engine_trainer import classify_new
from new.models import NewClassification
import requests


class NewClassificationViewSet(viewsets.ViewSet):
    queryset = NewClassification.objects.all()

    @staticmethod
    def list(request):
        return Response(data={':)'})

    @staticmethod
    def create(request):
        response_message = ""
        status_message = ""
        if 'new_id' in request.data:
            new_id = request.data['new_id']
            print(new_id)
            try:
                # Retrieve news from Nurdata
                url = 'http://corpus_data:4000/api/documents/?filters=[{"type": "match","field": "_id","value":"'\
                      + new_id + '"}]'
                data_request = requests.get(url)

                # Decode and formatting
                documents = data_request.json()
                new_data = documents['documents']['records']

                # Classify a new
                classify_status = classify_new(new_data)
                if classify_status == 200:
                    response_message = {"Classification succesfully!"}
                    status_message = status.HTTP_200_OK
                else:
                    response_message = {"Internal Error" : classify_status}
                    status_message = status.HTTP_500_INTERNAL_SERVER_ERROR
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

