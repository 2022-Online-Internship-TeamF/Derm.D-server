from .models import *
from .serializers import *

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

import jwt
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from django.conf import settings

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from django.http import JsonResponse
import json
from django.core import serializers


class QuestionListView(APIView):
    def filter_object_or_404(self, condition_id):
        try:
            return Question.objects.filter(condition=condition_id)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, condition_id):
        questions = self.filter_object_or_404(condition_id)
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



class LoginAPI(APIView): # 로그인
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data = data)
            if serializer.is_valid():
                nickname = serializer.data['nickname']
                password = serializer.data['password']

                user = authenticate(nickname=nickname, password=password)

                if user is None:
                    return Response({
                        'status': 400,
                        'message': '유저가 없거나 비밀번호 틀림',
                    })

                refresh = RefreshToken.for_user(user)
                refresh['nickname'] = user.nickname  # 확장

                res = Response()
                res.set_cookie('jwt', str(refresh))
                res.data = {
                    'status': 200,
                    'username': str(user.nickname),
                    'message': "로그인 완료",
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }

                return res

            return Response({
                'status' : 400,
                'message' : '잘못된 응답',
                'data' : serializer.errors
            })

        except Exception as e:
            print(e)

class RegisterAPI(APIView): # 회원가입
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data

        if User.objects.filter(nickname=request.data['nickname']).exists():  # 닉네임 중복 체크
            return Response({
                'status' : 400,
                'message': '중복되는 닉네임 입니다.'
            })
        elif User.objects.filter(email=request.data['email']).exists():  # 이메일 중복 체크
            return Response({
                'status' : 400,
                'message': '중복되는 이메일 입니다.'
            })

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'status': 200,
            'message': '회원가입 완료',
        })

class LogoutAPI(APIView): # 로그아웃
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('jwt')
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                'status': 205,
                'message': '로그아웃 성공',
            })
        except Exception as e:
            return Response({
                'status': 400,
                'message': '로그아웃 실패',
            })

class UserViewAPI(APIView) : #jwt로 닉네임 확인
  def get(self,request):
    token = request.COOKIES.get('jwt')

    if not token :
      raise AuthenticationFailed('UnAuthenticated!')

    try :
      SECRET_KEY = getattr(settings,'SECRET_KEY','localhost')
      payload = jwt.decode(token,SECRET_KEY,algorithms=['HS256'])

    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('UnAuthenticated!')

    user = User.objects.filter(id=payload['user_id']).first()
    serializer = idenSerializer(user)

    return Response(serializer.data)

def get_conditions_list(request): # 질환 확인
    conditions_list = Condition.objects.order_by('pk')[:100] # 오름차순 정렬.
    conditions_data = serializers.serialize("json", conditions_list, fields=('kr_name', 'eng_name', 'description'))
    conditions_data = json.loads(conditions_data)
    conditions_data = [{**item['fields'],**{"pk" : item['pk']}} for item in conditions_data]
    conditions_data = {
        "data" : conditions_data
    }
    return JsonResponse(conditions_data)