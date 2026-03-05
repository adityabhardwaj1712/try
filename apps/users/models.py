from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        user.set_password(password)

        user.save(using=self._db)

        return user


    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "ADMIN")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):

    username = None

    email = models.EmailField(unique=True)

    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("MANAGER", "Manager"),
        ("VIEWER", "Viewer"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="VIEWER"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def is_admin(self):
        return self.role == "ADMIN"

    def is_manager(self):
        return self.role == "MANAGER"

    def can_manage(self):
        return self.role in ["ADMIN", "MANAGER"]

    def __str__(self):
        return self.email