from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class MarqueVoiture(models.Model):
    marque = models.CharField(max_length=100)

    def __str__(self):
        return self.marque


class Modele(models.Model):
    nom = models.CharField(max_length=100)
    marque = models.ForeignKey(MarqueVoiture, on_delete=models.CASCADE, related_name='modeles')

    def __str__(self):
        return f"{self.marque} {self.nom}"


class Voiture(models.Model):
    
    modele = models.ForeignKey(Modele, on_delete=models.CASCADE)    
    TRANSMISSION_CHOICES = [
        ('Manuelle', 'Manuelle'),
        ('Automatique', 'Automatique'),
    ]
    TYPES_CARBURANT_CHOICES  = [
        ("Gasoil", "Gasoil"),
        ("Super", "Super"),
        ("Essence", "Essence"),
    ]
    nombre_de_vitesse = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(10)])
    annee_fabrication = models.PositiveIntegerField()
    kilometrage = models.PositiveIntegerField()
    type_carburant = models.CharField(choices=TYPES_CARBURANT_CHOICES,max_length=50)
    transmission = models.CharField(max_length=50, choices=TRANSMISSION_CHOICES)
    numero_serie = models.CharField(max_length=100)
    symptomes = models.TextField()
    couleur_voiture = models.CharField(max_length=50)
    historique_maintenance = models.TextField()
    codes_erreur = models.TextField(blank=True, null=True)
    photo_voiture = models.ImageField(upload_to="voitures/")
    numero_chassi = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.modele.marque} {self.modele} - {self.annee_fabrication}"




class Garage(models.Model):
    name = models.CharField(max_length=100)
    adresse = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100)
    site_web = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    horaire = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    photo_garage = models.ImageField(upload_to='photo_garage/')
    logo_garage = models.ImageField(upload_to='logo_garare/')
    
    status = models.BooleanField(default= True)
    date_add = models.DateTimeField(auto_now= True)
    date_update = models.DateTimeField(auto_now= True)

    def __str__(self) :
        return f"Garage -- {self.name}"