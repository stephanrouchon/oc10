from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from datetime import timedelta


AGE_MIN = 15

def validate_age(value):
    today = now().date()
    min_birth_date = today - timedelta(days=AGE_MIN*365)
    if value > min_birth_date:
        raise ValidationError("L'utilisateur doit avoir au moins quinze ans.")


class User(AbstractUser):
    
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    birthdate = models.DateField(validators=[validate_age])

    def age(self):

        today = now().date()
        return today.year - self.birthdate.year - ((today.month, today.day)<(
            self.birthdate.month, self.birthdate.day))

    def __str__(self):
        return self.username
