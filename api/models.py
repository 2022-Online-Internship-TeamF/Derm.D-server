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

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return '[Doctor : {}] {}'.format(self.doctor_flag, self.nickname)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Condition(BaseModel):

    CONDITION_CHOICE = [
        ('moles', 'Moles'),
        ('nevi', 'Nevi'),
        ('melanoma', 'Melanoma'),
        ('nail-disease', 'Nail Disease'),
        ('nail-fungus', 'Nail Fungus'),
        ('acne', 'Acne'),
        ('rosacea', 'Rosacea'),
        ('actinic-keratosis', 'Actinic Keratosis'),
        ('atopic-dermatitis', 'Atopic Dermatitis'),
        ('bacteria-infection', 'Bacteria Infection'),
        ('basal_insect', 'Basal Insect'),
        ('bullous', 'Bullous'),
        ('dermatofibroma', 'Dermatofibroma'),
        ('eczema', 'Eczema'),
        ('hemangloma', 'Hemangloma'),
        ('herpes', 'Herpes'),
        ('keratoses', 'Keratoses'),
        ('lichen-planus', 'Lichen Planus'),
        ('lupus', 'Lupus'),
        ('psoriasis', 'Psoriasis'),
        ('tinea', 'Tinea'),
        ('vasculitis', 'Vasculitis'),
        ('warts', 'Warts'),
    ]

    idx = models.IntegerField()
    kr_name = models.CharField(max_length=30, blank=True)
    eng_name = models.CharField(max_length=30, choices=CONDITION_CHOICE)
    definition = models.TextField(null=True, blank=True)
    cause = models.TextField(null=True, blank=True)
    treatment = models.TextField(null=True, blank=True)
    prevention = models.TextField(null=True, blank=True)
    guide = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    source = models.TextField(null=True, blank=True)
    symtom = models.TextField(null=True, blank=True)
    progress = models.TextField(null=True, blank=True)
    etc = models.TextField(null=True, blank=True)

    def __str__(self):
        return '{} ({})'.format(self.kr_name, self.eng_name)


class Archive(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_archive')
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE, related_name='condition_archive')

    def __str__(self):
        return '[User : {}] {}'.format(self.user.nickname, self.condition.eng_name)


class Question(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_question')
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE, related_name='condition_question')

    content = models.TextField()

    def __str__(self):
        return '[{} : Q{}] - {}'.format(self.condition.eng_name, self.id, self.user.nickname)


class Answer(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_answer')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_answer')
    # hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='answer')

    content = models.TextField()

    def __str__(self):
        return '[{} : Q{}] - A{} by {}'.format(self.question.condition.eng_name, self.question.id, self.id, self.user.nickname)


def condition_media_path(instance, filename):
    return f'{instance.condition.eng_name}/condition/{filename}'


def question_media_path(instance, filename):
    return f'{instance.question.condition.eng_name}/qna/{instance.question.id}/question/{filename}'


def answer_media_path(instance, filename):
    return f'{instance.answer.question.condition.eng_name}/qna/{instance.answer.question.id}/answer/{filename}'


class ConditionMedia(BaseModel):
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE, related_name='condition_conditionmedia')
    img = models.ImageField(upload_to=condition_media_path, blank=True)
    main_flag = models.BooleanField(default=False)

    def __str__(self):
        return '{} ({}) - (Main : {})'.format(self.condition.kr_name, self.condition.eng_name, self.main_flag)


class QuestionMedia(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_questionmedia')

    img = models.ImageField(upload_to=question_media_path, blank=True)
    main_flag = models.BooleanField(default=False)

    def __str__(self):
        return '[{} : Q{}] - {} (Main : {})'.format(self.question.condition.eng_name, self.question.id, self.question.user.nickname, self.main_flag)


class AnswerMedia(BaseModel):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_answermedia')

    img = models.ImageField(upload_to=answer_media_path, blank=True)
    main_flag = models.BooleanField(default=False)

    def __str__(self):
        return '[{} : Q{}] - A{} by {} (Main : {})'.format(self.answer.question.condition.eng_name, self.answer.question.id, self.answer.id, self.answer.user.nickname, self.main_flag)
