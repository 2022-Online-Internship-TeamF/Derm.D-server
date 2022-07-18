from django.urls import path
from .views import *


urlpatterns = [
    path('condition/<int:condition_id>/question/', QuestionListView.as_view()),
    path('condition/<int:condition_id>/question/<int:question_id>/', QuestionDetailView.as_view())
]