from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, verbose_name='학번')

    def __str__(self):
        return f'{self.user.username} ({self.student_id})'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, verbose_name='학번')
    views_made = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} ({self.student_id})'