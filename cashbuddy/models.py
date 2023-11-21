import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None, country=None, phone_number=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name, country=country, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, first_name, last_name, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    country = models.CharField(max_length=50)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # password_reset_otp = models.CharField(max_length=6, null=True, blank=True)
    # otp_timestamp = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'country']

    class Meta:
        verbose_name = 'Cashbuddy User'  # Set the verbose name here

    def __str__(self):
        return self.username
    
class PasswordResetCode(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    timestamp = models.DateTimeField(default=timezone.now)

    def is_expired(self):
        expiration_time = self.timestamp + timezone.timedelta(minutes=15)
        return timezone.now() > expiration_time


class Transaction(models.Model):
    title = models.CharField(max_length=255)
    details = models.TextField()
    category = models.CharField(max_length=50)
    transaction_type = models.CharField(max_length=20, choices=[('income', 'Income'), ('expense', 'Expense')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return self.title

class BudgetPlanCategory(models.Model):
    category_title = models.CharField(max_length=255)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.category_title

    class Meta:
        verbose_name_plural = "Budget Plan Categories"

class BudgetPlan(models.Model):
    title = models.CharField(max_length=255)
    categories = models.ManyToManyField(BudgetPlanCategory)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Budget Plans"

class Notification(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    body = models.TextField()

    def __str__(self):
        return self.title

class Report(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.title