from .serializers import NewClassifiedSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from TMengine.engine_trainer import classify_new
from new.models import NewClassification, New
import json


class NewViewSet(viewsets.ViewSet):

    @staticmethod
    def list(request):
        news = New.objects.all()
        print(news)
        response_json = []
        response_status = ""
        try:
            for new in news:
                serialized_topic = NewClassifiedSerializer(new).data
                response_json.append(serialized_topic)
                response_status = status.HTTP_200_OK
        except Exception as e:
            response_json = {"Exception raised": e}
            response_status = status.HTTP_404_NOT_FOUND
        return Response(data=response_json, status=response_status)

    @staticmethod
    def create(request):
        response_message = classify_new(request.data)
        response_status = status.HTTP_200_OK
        return Response(data={"message": response_message}, status=response_status)

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


new_list = NewViewSet.as_view({
    'view': 'list',
    'post': 'create',
    'get': 'list',
})
