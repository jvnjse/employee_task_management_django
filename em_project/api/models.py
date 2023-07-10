from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    qr_code_image = models.ImageField(upload_to="qr_codes/", blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    groups = models.ManyToManyField("auth.Group", related_name="custom_users")
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="custom_users"
    )


class Job(models.Model):
    STATUS_CHOICES = (
        ("NOT_STARTED", "Not Started"),
        ("IN_PROGRESS", "In Progress"),
        ("CHECKING", "Checking On It"),
        ("DONE", "Done"),
        ("STARTED_WORKING", "Started Working"),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    comments = models.TextField(blank=True, null=True)
    employees = models.ManyToManyField(CustomUser, related_name="jobs_assigned")
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    submission_date = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="NOT_STARTED"
    )

    def __str__(self):
        return self.title
