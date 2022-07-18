from .models import *
from .serializers import *

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404


class QuestionListView(APIView):
    def get(self, request, condition_id):
        questions = Question.objects.filter(condition=condition_id)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class QuestionDetailView(APIView):
    def get_object_or_404(self, condition_id, question_id):
        try:
            return Question.objects.get(condition=condition_id, pk=question_id)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, condition_id, question_id):
        question = self.get_object_or_404(condition_id, question_id)
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, condition_id, question_id):
        question = self.get_object_or_404(condition_id, question_id)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)