from .serializers import PreprocessedDataSerializer, NewClassifiedSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from TMengine.engine_trainer import classify_new
from new.models import NewClassification
from topic.models import Topic
from TMengine.models import LdaModel


class NewViewSet(viewsets.ViewSet):

    @staticmethod
    def list(request):
        news = NewClassification.objects.all()
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
        data = request.data["documents"]
        response_message = ""
        response_status = ""
        for new in data:
            data_serialized = PreprocessedDataSerializer(data=new)
            try:
                if data_serialized.is_valid():
                    new_object = data_serialized.save()
                    classifications = classify_new(new_object.text)
                    for classification in classifications["classifications"]:
                        lda_model = LdaModel.objects.get(pk=classifications['id_model'])
                        topic = Topic.objects.get(topic_number=classification[0],
                                                  lda_model=lda_model)
                        NewClassification(
                            classification=classification[0],
                            new_id=new_object,
                            topic_id=topic
                        ).save()
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
    'get': 'list',
})
