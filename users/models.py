from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('이메일은 필수 입력사항 입니다!')
        
        if not username:
            raise ValueError('닉네임은 필수 입력사항 입니다!')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    email_valid = models.BooleanField(default=False)
    username = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_login = models.DateTimeField(auto_now=True, null=True, blank=True)
    provider = models.CharField(max_length=50, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
