from django.urls import path
from .views import *

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [

    path('token/refresh', TokenRefreshView.as_view()),

    path('user/register', RegisterView.as_view()),
    path('user/login', LoginView.as_view()),
    path('user/logout', LogoutView.as_view()),

    path('user', UserDetailView.as_view()),

    path('user/archive', ArchiveListView.as_view()),
    path('user/archive/<int:archive_id>', ArchiveDeleteView.as_view()),

    path('condition', ConditionListView.as_view()),

    path('condition/<str:condition_name>', ConditionDetailView.as_view()),

    path('condition/<str:condition_name>/question', QuestionListView.as_view()),
    path('condition/<str:condition_name>/question/<int:question_id>', QuestionDetailView.as_view()),

    path('condition/<str:condition_name>/question/<int:question_id>/answer', AnswerListView.as_view()),
    path('condition/<str:condition_name>/question/<int:question_id>/answer/<int:answer_id>', AnswerDetailView.as_view()),

]
