from topic.models import Topic, Keyword
from TMengine.models import LdaModel
from new.models import New
from TMengine.engine_trainer import update_model
from rest_framework import viewsets, status
from rest_framework.response import Response


class LdaModelViewSet(viewsets.ViewSet):

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
            news = list(New.objects.all().values_list('text', flat=True))
            new_filename, new_topics = update_model(news)
            ldamodel_instance = LdaModel.objects.get(filename=new_filename)
            for topic in new_topics:
                topic_instance = Topic(topic_number=topic['topic_number'],
                                       lda_model=ldamodel_instance)
                topic_instance.save()
                for keyword in topic["keywords"]:
                    keyword_instance = Keyword(name=keyword['name'],
                                               weight=keyword['weight'],
                                               topic_id=topic_instance)
                    keyword_instance.save()
            response_message = {"Model updated successfully!, new filename: " + new_filename}
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
})
