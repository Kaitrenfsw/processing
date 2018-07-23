from .serializers import PreprocessedDataSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from TMengine.engine_trainer import classify_new


class NewViewSet(viewsets.ViewSet):

    @staticmethod
    def list(request):
        topic_ids = request.data["topic_ids"]
        print(topic_ids)
        return Response(data={":)"})

    @staticmethod
    def create(request):
        data = request.data
        data_serialized = PreprocessedDataSerializer(data=data["documents"], many=True)
        print(classify_new(data["documents"][0]["text"]))
        try:
            if data_serialized.is_valid():
                data_serialized.save()
                response_message = "Data saved succesfully!"
                response_status = status.HTTP_200_OK
            else:
                response_message = "Wrong request format!"
                response_status = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            response_message = {"Exception raised": e}
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
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
})
