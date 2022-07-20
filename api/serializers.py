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
    answerMedia = AnswerMediaSerializer(many=True)

    class Meta:
        model = Answer
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    # answers = AnswerSerializer(many=True)
    questionMedia = QuestionMediaSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'


class ArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archive
        fields = '__all__'


class ConditionSerializer(serializers.ModelSerializer):
    archives = ArchiveSerializer(many=True)
    questions = QuestionSerializer(many=True)
    conditionMedia = ConditionMediaSerializer(many=True)
    questionMedia = QuestionMediaSerializer(many=True)

    class Meta:
        model = Condition
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    # archives = ArchiveSerializer(many=True)
    # questions = QuestionSerializer(many=True)
    # answers = AnswerSerializer(many=True)
    class Meta:
        model = User
        fields = '__all__'


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
