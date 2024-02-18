from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        if not first_name:
            raise ValueError("Users must have a first name")

        if not last_name:
            raise ValueError("Users must have a last name")

        falcon_ai_user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        falcon_ai_user.set_password(password)
        falcon_ai_user.save()
        return falcon_ai_user

    def create_superuser(self, email, first_name, last_name, password=None):
        falcon_ai_user = self.create_user(
            email, first_name, last_name, password=password
        )
        falcon_ai_user.is_admin = True
        falcon_ai_user.set_password(password)
        falcon_ai_user.save()
        return falcon_ai_user


class FlaconAIUser(AbstractBaseUser):
    username = None
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Business(models.Model):
    business_id = models.CharField(max_length=100, null=False, primary_key=True)
    name = models.CharField(max_length=100, null=False)


class Employee(models.Model):
    employee_id = models.CharField(max_length=100, null=False, primary_key=True)
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.email


class Campaign(models.Model):
    campaign_id = models.CharField(max_length=100, null=False, primary_key=True)
    start_date = models.DateTimeField(default=timezone.now, blank=False, null=False)
    end_date = models.DateTimeField(blank=False, null=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.campaign_id


class AIEmail(models.Model):
    class WritingStyle(models.IntegerChoices):
        FORMAL = 0
        APPRECIATING = 1
        NOT_SATISFIED = 2
        NEUTRAL = 3

    email_id = models.CharField(max_length=100, null=False, primary_key=True)
    campaign = models.ForeignKey(Campaign, null=True, on_delete=models.CASCADE)
    email_topic = models.CharField(max_length=500, null=True)
    sender = models.ForeignKey(FlaconAIUser, null=True, on_delete=models.PROTECT)
    recipient = models.ForeignKey(Employee, null=True, on_delete=models.PROTECT)
    writing_style = models.IntegerField(
        verbose_name="writing style",
        choices=WritingStyle.choices,
        default=WritingStyle.FORMAL,
        null=True,
    )
    email_content = models.TextField(null=False)

    def __str__(self):
        return self.email_id


class EmployeeAction(models.Model):
    class Action(models.IntegerChoices):
        CLICK = 0
        VIEW = 1

    action_id = models.CharField(max_length=100, null=False, primary_key=True)
    # change it to non-nullable after Employee creation backend completed
    employee = models.ForeignKey(Employee, null=True, on_delete=models.CASCADE)
    email = models.ForeignKey(AIEmail, null=True, on_delete=models.CASCADE)
    action = models.IntegerField(
        verbose_name="action",
        choices=Action.choices,
        default=Action.CLICK,
        null=True,
    )

    def __str__(self):
        return self.action_id
