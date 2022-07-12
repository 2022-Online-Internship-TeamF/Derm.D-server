from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)


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

    LEVEL_CHOICE = [
        ('Ruby', 'Ruby'),
        ('Diamond', 'Diamond'),
        ('Platinum', 'Platinum'),
        ('Gold', 'Gold'),
        ('Silver', 'Silver'),
        ('Bronze', 'Bronze'),
    ]

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
        return '[{}] {}'.format(self.doctor_flag, self.nickname)
