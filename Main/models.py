from django.db import models

# Create your models here.
class envoi_contact(models.Model):
    nom = models.CharField(max_length=12)
    email = models.EmailField()
    message = models.TextField()

    # standards
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self) :
        return f"Message de {self.nom}"