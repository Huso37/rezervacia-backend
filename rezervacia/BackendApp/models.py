from django.db import models

# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)

    class Meta:
        db_table = 'users'  # Map to the existing `users` table