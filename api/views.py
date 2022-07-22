from .serializers import *

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


# 사용자 정보
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        cur_user = request.user

        if cur_user.is_anonymous:
            return Response({
                "user": "User Not Found"
            }, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = UserSerializer(request.user)
            return Response({
                "user": serializer.data,
            }, status=status.HTTP_200_OK)


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


class LoginAPI(APIView):  # 로그인
    # noinspection PyMethodMayBeStatic
    def post(self, request):
        try:
            data = request.data  # 입력된 데이터를 data 저장.
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():  # 유효성 검사 -> serialize 저장 가능
                nickname = serializer.data['nickname']
                password = serializer.data['password']

                user = authenticate(nickname=nickname, password=password)  # 회원 정보 확인.

                if user is None:  # 회원 정보가 일치하지 않거나 없다면 오류 메시지
                    return Response({
                        'message': '유저가 없거나 비밀번호 틀림'
                    }, status=status.HTTP_400_BAD_REQUEST)

                refresh = RefreshToken.for_user(user)  # 유저 정보로 refresh 토큰 생성
                refresh['nickname'] = user.nickname  # refresh 토큰에 nickname 값 추가로 입력

                res = Response()  # cookie 넣기 위해 Response 사용
                res.set_cookie('jwt', str(refresh))  # jwt이름의 쿠키 value refresh 토큰으로 설정

                res.data = {
                    'username': str(user.nickname),
                    'message': "로그인 완료",
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
                return res

            return Response({
                'message': '잘못된 응답'
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class RegisterAPI(APIView):  # 회원가입
    # noinspection PyMethodMayBeStatic
    def post(self, request):
        try:
            user = request.data  # 입력된 데이터를 user 저장.

            serializer = RegistrationSerializer(data=user)
            if User.objects.filter(nickname=request.data['nickname']).exists():  # 닉네임 중복 체크
                return Response({
                    'message': '중복되는 닉네임 입니다.'
                }, status=status.HTTP_400_BAD_REQUEST)
            elif User.objects.filter(email=request.data['email']).exists():  # 이메일 중복 체크
                return Response({
                    'message': '중복되는 이메일 입니다.'
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.is_valid()
            serializer.save()
            return Response({
                'message': '회원가입 완료',
            }, status=status.HTTP_200_OK)
        except Exception as e:  # 예외처리
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPI(APIView):  # 로그아웃
    # noinspection PyMethodMayBeStatic
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('jwt')
            if not refresh_token:
                return Response({
                    'message': '토큰이 없습니다.',
                }, status=status.HTTP_400_BAD_REQUEST)
            res = Response()
            res.delete_cookie('jwt')
            token = RefreshToken(refresh_token)
            token.blacklist()

            res.data = {'message': "로그아웃 완료"}

            return res
        except Exception as e:  # 예외처리
            return Response({
                'message': str(e),
            }, status=status.HTTP_400_BAD_REQUEST)


class ConditionListView(APIView):
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        conditions = Condition.objects.all()
        serializer = ConditionSerializer(conditions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConditionDetailView(APIView):
    # noinspection PyMethodMayBeStatic
    def get_object_or_404(self, pk):
        try:
            return Condition.objects.get(pk=pk)
        except Condition.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        condition = self.get_object_or_404(pk)
        serializer = ConditionSerializer(condition)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 아카이브 리스트 출력 및 저장
class ArchiveListView(APIView):
    # noinspection PyMethodMayBeStatic
    def get_object_or_404(self, name):
        try:
            return Condition.objects.get(kr_name=name).pk
        except Condition.DoesNotExist:
            raise Http404

    # noinspection PyMethodMayBeStatic
    def filter_object_or_404(self, id):
        try:
            return Archive.objects.filter(user=id)
        except Archive.DoesNotExist:
            raise Http404

    def get(self, request):
        user = request.user
        archives = self.filter_object_or_404(user.id)
        serializer = ArchiveSerializer(archives, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        data = request.data
        data["user"] = user.id
        data["condition"] = self.get_object_or_404(data["condition"])
        if Archive.objects.filter(condition=request.data['condition']).exists():  # 같은 증상 중복 체크
            return Response({
                'message': '중복되는 아카이브가 있습니다.'
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer = ArchiveAddSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# 아카이브 삭제기능
class ArchiveDeleteView(APIView):
    # noinspection PyMethodMayBeStatic
    def get_object_or_404(self, archive_id):
        try:
            return Archive.objects.get(pk=archive_id)
        except Archive.DoesNotExist:
            raise Http404

    def delete(self, request, archive_id):
        archive = self.get_object_or_404(archive_id)
        archive.delete()
        return Response({
            'message': '삭제 성공'
        }, status=status.HTTP_204_NO_CONTENT)