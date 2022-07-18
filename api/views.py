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