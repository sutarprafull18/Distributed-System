from django.db import models
from django.core.exceptions import ValidationError
import re

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    class Meta:
        app_label = 'users_app'

    def clean(self):
        if not self.name:
            raise ValidationError('Name is required')
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.email):
            raise ValidationError('Invalid email format')

    def __str__(self):
        return f"{self.name} ({self.email})"

