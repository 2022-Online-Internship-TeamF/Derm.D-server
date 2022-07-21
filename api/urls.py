from django.urls import path
from .views import *

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('condition/<int:condition_id>/question/', QuestionListView.as_view()),
    path('condition/<int:condition_id>/question/<int:question_id>/', QuestionDetailView.as_view()),

    path('members/login/', LoginAPI.as_view()),
    path('members/register/', RegisterAPI.as_view()),
    path('members/logout/', LogoutAPI.as_view()),
    path('members/refresh/', TokenRefreshView.as_view()),  # access 토큰 재 발급
    path('members/nickname/', TokenNickname.as_view()),  # 쿠키(토큰)에서 닉네임 가져오기.

    path('condition/', ConditionListView.as_view()),
    path('condition/<int:pk>/', ConditionDetailView.as_view())
]
