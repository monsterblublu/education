from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    MEMBER_CHOICHES = (
        ('TEACHER', 'I am teacher'),
        ('STUDENT', 'I am student')
    )
    email = models.EmailField(unique=True)
    role = models.CharField('teacher', choices=MEMBER_CHOICHES,
                                     max_length=10, default='STUDENT')

    def __str__(self):
        return self.first_name + " " + self.last_name
