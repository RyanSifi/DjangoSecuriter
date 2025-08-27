from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from secure_auth.secure_auth import settings


class CustomUserManager(UserManager):
    def normalize_email(self, email):
        return super().normalize_email(email)

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'email doit étre renseignée')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    failed_login_attempts = models.IntegerField(default=0)
    account_locked_until = models.DateTimeField(null=True, blank=True)
    last_password_change = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Document(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)

    class Meta:
        permissions = [
            ("publish_document", "Can publish documents"),
            ("review_document", "Can review documents"),
        ]

    def __str__(self):
        return self.title

    def user_can_edit(self, user):
        return user == self.owner or user.has_perm('accounts.change_document')

    def user_can_delete(self, user):
        return user == self.owner or user.has_perm('accounts.delete_document')