from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)


# class Hosptial(models.Model):
# 기능 추가 시 병원 모델 추가


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, nickname, password=None):
        if not email:
            raise ValueError('User must have email')
        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password):
        user = self.create_user(
            email=self.normalize_email(email),
            nickname=nickname,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    objects = UserManager()

    nickname = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=200, unique=True)

    doctor_flag = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return '[Doctor : {}] {}'.format(self.doctor_flag, self.nickname)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Condition(BaseModel):
    kr_name = models.CharField(max_length=30, blank=True)
    eng_name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return '{} ({})'.format(self.kr_name, self.eng_name)


class Archive(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='archive')
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE, related_name='archive')

    def __str__(self):
        return '[User : {}] {}'.format(self.user.nickname, self.condition.eng_name)


class Question(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question')
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE, related_name='question')

    content = models.TextField()

    def __str__(self):
        return '[{} : Q{}] - {}'.format(self.condition.eng_name, self.id, self.user.nickname)


class Answer(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer')
    # hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='answer')

    content = models.TextField()

    def __str__(self):
        return '[{} : Q{}] - A{} by {}'.format(self.question.condition.eng_name, self.question.id, self.id, self.user.nickname)


class ConditionMedia(BaseModel):
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE, related_name='conditionMedia')

    img = models.ImageField(blank=True)
    main_flag = models.BooleanField(default=False)

    def __str__(self):
        return '{} ({}) - (Main : {})'.format(self.condition.kr_name, self.condition.eng_name, self.main_flag)


class QuestionMedia(BaseModel):
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE, related_name='questionMedia')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='questionMedia')

    img = models.ImageField(blank=True)
    main_flag = models.BooleanField(default=False)

    def __str__(self):
        return '[{} : Q{}] - {} (Main : {})'.format(self.condition.eng_name, self.question.id, self.question.user.nickname, self.main_flag)


class AnswerMedia(BaseModel):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answerMedia')

    img = models.ImageField(blank=True)
    main_flag = models.BooleanField(default=False)

    def __str__(self):
        return '[{} : Q{}] - A{} by {} (Main : {})'.format(self.answer.question.condition.eng_name, self.answer.question.id, self.answer.id, self.answer.user.nickname, self.main_flag)
