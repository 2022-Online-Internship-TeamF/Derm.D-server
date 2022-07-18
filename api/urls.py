from django.urls import path

from . import views
from .views import *

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('condition/<int:condition_id>/question/', QuestionListView.as_view()),
    path('condition/<int:condition_id>/question/<int:question_id>/', QuestionDetailView.as_view()),

    path('members/login/', LoginAPI.as_view()),
    path('members/register/', RegisterAPI.as_view()),
    path('members/logout/', LogoutAPI.as_view()),
    path('members/nickname/', UserViewAPI.as_view()),
    path('members/refresh/', TokenRefreshView.as_view()),  # 토큰 재발급하기

    path('condition/', condition_listAPI.as_view()),
    path('condition/<int:pk>/', condition_detailAPI.as_view())
]