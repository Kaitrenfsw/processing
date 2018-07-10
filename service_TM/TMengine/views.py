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
        print(data["document"][0])
        response_message = document_classifier(data["document"][0])
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

    @staticmethod
    def classify_new(request):
        data = request.data
        print(data["documents"][0])
        response_message = document_classifier(data["documents"][0]["text"])
        return Response(data=response_message)


lda_model_list = LdaModelViewSet.as_view({
    'get': 'list',
    'post': 'classify_new',
    'put': 'update',
})


