from django.urls import path
from .views import *

from . import views

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('condition/<int:condition_id>/question/', QuestionListView.as_view()),
    path('condition/<int:condition_id>/question/<int:question_id>/', QuestionDetailView.as_view()),

    path('members/login/', LoginAPI.as_view()),
    path('members/register/', RegisterAPI.as_view()),
    path('members/logout/', LogoutAPI.as_view()),
    path('members/nickname/', UserViewAPI.as_view()),
    path('members/refresh/', TokenRefreshView.as_view()),  # 토큰 재발급하기

    path('conditions', views.get_conditions_list, name='get_conditions_list'),
]