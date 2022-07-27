from .serializers import *
from .models import *
from .forms import *

from django.http import Http404
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


# 사용자 정보
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_anonymous:
            return Response({
                "user": "User Not Found"
            }, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = UserSerializer(request.user)
            return Response({
                "user": {
                    "nickname": serializer.data["nickname"],
                    "email": serializer.data["email"],
                    "doctor": serializer.data["doctor_flag"],
                }
            }, status=status.HTTP_200_OK)


class ArchiveListView(APIView):
    def filter_object_or_404(self, id):
        try:
            return Archive.objects.filter(user=id)
        except Archive.DoesNotExist:
            raise Http404

    def get(self, request):
        archives = self.filter_object_or_404(request.user.id)
        serializer = ArchiveSerializer(archives, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionListView(APIView):
    def filter_object_or_404(self, condition_name):
        try:
            return Question.objects.filter(condition__eng_name=condition_name)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, condition_name):
        questions = self.filter_object_or_404(condition_name)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, condition_name):

        user = User.objects.get(id=request.user.id)
        condition = Condition.objects.get(eng_name=condition_name)
        content = request.data["content"]

        data = {
            "user": user,
            "condition": condition,
            "content": content,
        }

        form = QuestionForm(data=data)

        if form.is_valid():
            question = form.save()

            for index, file in enumerate(request.FILES.getlist('media')):
                question_media = QuestionMedia()
                question_media.question = question
                question_media.img = file
                if index is 0:
                    question_media.main_flag = True
                question_media.save()

            return Response("Question Submitted", status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailView(APIView):
    def get_object_or_404(self, condition_name, question_id):
        try:
            return Question.objects.get(condition__eng_name=condition_name, id=question_id)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, condition_name, question_id):
        question = self.get_object_or_404(condition_name, question_id)
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, condition_name, question_id):
        cur_question = self.get_object_or_404(condition_name, question_id)
        cur_question_media = QuestionMedia.objects.filter(question__id=question_id)

        user = User.objects.get(id=request.user.id)
        condition = Condition.objects.get(eng_name=condition_name)
        content = request.data["content"]

        data = {
            "user": user,
            "condition": condition,
            "content": content,
        }

        if cur_question.user == request.user:

            form = QuestionForm(data=data, instance=cur_question)

            if form.is_valid():
                question = form.save()

                for index, file in enumerate(request.FILES.getlist('media')):
                    cur_question_media.delete()

                    question_media = QuestionMedia()
                    question_media.question = question
                    question_media.img = file
                    if index is 0:
                        question_media.main_flag = True
                    question_media.save()

                return Response("Question Edited", status=status.HTTP_201_CREATED)
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, condition_name, question_id):
        question = self.get_object_or_404(condition_name, question_id)

        if question.user == request.user:
            question.delete()

            return Response(f"Q{question_id} Deleted", status=status.HTTP_200_OK)
        return Response("Not allowed user", status=status.HTTP_400_BAD_REQUEST)


class AnswerListView(APIView):
    def filter_object_or_404(self, condition_name, question_id):
        try:
            return Answer.objects.filter(question__condition__eng_name=condition_name, question__id=question_id)
        except Answer.DoesNotExist:
            raise Http404

    def get(self, request, condition_name, question_id):
        answers = self.filter_object_or_404(condition_name, question_id)
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, condition_name, question_id):

        try:
            user = User.objects.get(id=request.user.id, doctor_flag=True)

        except:
            return Response({"This user is not a doctor"}, status=status.HTTP_400_BAD_REQUEST)

        question = Question.objects.get(id=question_id)
        content = request.data["content"]

        data = {
            "user": user,
            "question": question,
            "content": content,
        }

        form = AnswerForm(data=data)

        if form.is_valid():
            answer = form.save()

            for index, file in enumerate(request.FILES.getlist('media')):
                answer_media = AnswerMedia()
                answer_media.answer = answer
                answer_media.img = file
                if index is 0:
                    answer_media.main_flag = True
                answer_media.save()

            return Response("Answer Submitted", status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswerDetailView(APIView):
    def get_object_or_404(self, condition_name, question_id, answer_id):
        try:
            return Answer.objects.get(question__condition__eng_name=condition_name, question__id=question_id, id=answer_id)
        except Answer.DoesNotExist:
            raise Http404

    def get(self, request, condition_name, question_id, answer_id):
        answer = self.get_object_or_404(condition_name, question_id, answer_id)
        serializer = AnswerSerializer(answer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, condition_name, question_id, answer_id):

        try:
            user = User.objects.get(id=request.user.id, doctor_flag=True)

        except:
            return Response({"This user is not a doctor"}, status=status.HTTP_400_BAD_REQUEST)

        cur_answer = self.get_object_or_404(condition_name, question_id, answer_id)
        cur_answer_media = AnswerMedia.objects.filter(answer__id=answer_id)

        question = Question.objects.get(id=question_id)
        content = request.data["content"]

        data = {
            "user": user,
            "question": question,
            "content": content,
        }

        if cur_answer.user == request.user:

            form = AnswerForm(data=data, instance=cur_answer)

            if form.is_valid():
                answer = form.save()

                for index, file in enumerate(request.FILES.getlist('media')):
                    cur_answer_media.delete()

                    answer_media = AnswerMedia()
                    answer_media.answer = answer
                    answer_media.img = file
                    if index is 0:
                        answer_media.main_flag = True
                    answer_media.save()

                return Response("Answer Edited", status=status.HTTP_201_CREATED)
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, condition_name, question_id, answer_id):

        try:
            user = User.objects.get(id=request.user.id, doctor_flag=True)

        except:
            return Response({"This user is not a doctor"}, status=status.HTTP_400_BAD_REQUEST)

        answer = self.get_object_or_404(condition_name, question_id, answer_id)

        if answer.user == request.user:
            answer.delete()

            return Response(f"A{answer_id} Deleted", status=status.HTTP_200_OK)
        return Response("Not allowed user", status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):  # 로그인
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


class RegisterView(APIView):  # 회원가입
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


class LogoutView(APIView):  # 로그아웃
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
    def get(self, request):
        conditions = Condition.objects.all()
        serializer = ConditionMiniSerializer(conditions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConditionDetailView(APIView):
    def get_object_or_404(self, condition_name):
        try:
            return Condition.objects.get(eng_name=condition_name)
        except Condition.DoesNotExist:
            raise Http404

    def get(self, request, condition_name):
        condition = self.get_object_or_404(condition_name)
        serializer = ConditionSerializer(condition)
        return Response(serializer.data, status=status.HTTP_200_OK)
