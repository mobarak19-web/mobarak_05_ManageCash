from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Custom User Model
class CustomUser(AbstractUser):
    display_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.display_name


# Add Cash Model
class AddCash(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cash"
    )
    source = models.CharField(max_length=255, null=True, blank=True)
    datetime = models.DateTimeField()
    amount = models.IntegerField(null=True, blank=True)
    description = models.TextField(max_length=255)

    def __str__(self):
        return f"{self.source} - {self.amount} - {self.user.username}"


# Expense Model
class Expense(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="expenses"
    )
    datetime = models.DateTimeField()
    amount = models.IntegerField(null=True, blank=True)
    description = models.TextField(max_length=255)

    def __str__(self):
        return f"{self.amount} - {self.description} - {self.user.username}"
    
    