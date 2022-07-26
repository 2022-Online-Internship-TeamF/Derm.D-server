from django.urls import path
from .views import *

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [

    path('user/refresh', TokenRefreshView.as_view()),

    path('user/register', RegisterView.as_view()),
    path('user/login', LoginView.as_view()),
    path('user/logout', LogoutView.as_view()),

    path('user', UserDetailView.as_view()),

    path('condition', ConditionListView.as_view()),
    path('condition/<int:pk>', ConditionDetailView.as_view()),

    path('condition/<int:condition_id>/question', QuestionListView.as_view()),
    path('condition/<int:condition_id>/question/<int:question_id>', QuestionDetailView.as_view()),

]
