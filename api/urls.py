from django.urls import path
from .views import *

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('user', UserDetailView.as_view()),

    path('condition/<int:condition_id>/question/', QuestionListView.as_view()),
    path('condition/<int:condition_id>/question/<int:question_id>/', QuestionDetailView.as_view()),

    path('members/login/', LoginAPI.as_view()),
    path('members/register/', RegisterAPI.as_view()),
    path('members/logout/', LogoutAPI.as_view()),
    path('members/refresh/', TokenRefreshView.as_view()),  # access 토큰 재 발급

    path('archive/', ArchiveListView.as_view()),
    path('archive/<int:archive_id>/', ArchiveDeleteView.as_view()),

    path('condition/', ConditionListView.as_view()),
    path('condition/<int:pk>/', ConditionDetailView.as_view())
]
