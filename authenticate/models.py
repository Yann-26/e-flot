from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class type_client(models.Model):
    TYPECHOICES = (
        ('Particulier', 'Particulier'),
        ('Entreprise', 'Entreprise'),
        ('Garage', 'Garage'),
    )
    type = models.CharField(choices=TYPECHOICES, max_length=20)

    def __str__(self):
        return self.type



class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    termes_accept = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True, null=True)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username