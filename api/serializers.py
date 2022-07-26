from rest_framework import serializers
from .models import *


class AnswerMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerMedia
        fields = '__all__'


class QuestionMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionMedia
        fields = '__all__'


class ConditionMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConditionMedia
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    answer_answermedia = AnswerMediaSerializer(many=True)

    class Meta:
        model = Answer
        fields = [
            'id',
            'question',
            'user',
            'content',
            'created_at',
            'modified_at',
            'answer_answermedia',
        ]


class QuestionSerializer(serializers.ModelSerializer):
    question_questionmedia = QuestionMediaSerializer(many=True)
    # question_answer = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = [
            'id',
            'user',
            'condition',
            'content',
            'created_at',
            'modified_at',
            'question_questionmedia',
            # 'question_answer',
        ]


class ArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archive
        fields = '__all__'


class ConditionSerializer(serializers.ModelSerializer):
    condition_conditionmedia = ConditionMediaSerializer(many=True)

    class Meta:
        model = Condition
        fields = [
            'id',
            'idx',
            'kr_name',
            'eng_name',
            'definition',
            'cause',
            'treatment',
            'prevention',
            'guide',
            'summary',
            'source',
            'symtom',
            'progress',
            'etc',
            'condition_conditionmedia',
        ]


class ConditionMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Condition
        fields = [
            'kr_name',
            'eng_name',
        ]


class UserSerializer(serializers.ModelSerializer):
    user_archive = ArchiveSerializer(many=True)
    user_question = QuestionSerializer(many=True)
    user_answer = AnswerSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'id',
            'nickname',
            'email',
            'doctor_flag',
            'user_archive',
            'user_question',
            'user_answer',
        ]


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'password', 'email', 'doctor_flag']

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            # provide django, password will be hashing!
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['nickname', 'password']
