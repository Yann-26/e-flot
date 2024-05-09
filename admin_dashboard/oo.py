from django.db import models

class Marque(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom
    
MARQUES = [
    "Abarth", "Acura", "Aixam", "Alfa Romeo", "Alpina", "Alpine", "Ariel", "Aston Martin",
    "Audi", "Austin", "Autobianchi", "Bentley", "BMW", "Borgward", "Bugatti", "Buick", "Cadillac",
    "Caterham", "Chevrolet", "Chrysler", "Citroën", "Corvette", "Cupra", "Dacia", "Daewoo",
    "Daihatsu", "Datsun", "De Tomaso", "Delahaye", "DeLorean", "Dodge", "DS Automobiles", "Eagle",
    "Ferrari", "Fiat", "Fisker", "Ford", "Genesis", "Ginetta", "GMC", "Holden", "Honda", "Hummer",
    "Hyundai", "Infiniti", "Innocenti", "Isuzu", "Jaguar", "Jeep", "Jensen", "Kia", "Koenigsegg",
    "Lada", "Lamborghini", "Lancia", "Land Rover", "Lexus", "Ligier", "Lincoln", "Lotus", "Mahindra",
    "Maserati", "Maybach", "Mazda", "McLaren", "Mercedes-Benz", "MG", "MINI", "Mitsubishi", "Morgan",
    "Moskvitch", "Nissan", "Noble", "NSU", "Oldsmobile", "Opel", "Pagani", "Panoz", "Peugeot", "Plymouth",
    "Polestar", "Pontiac", "Porsche", "Proton", "Puma", "Qoros", "RAM", "Reliant", "Renault", "Rezvani",
    "Rimac", "Rolls-Royce", "Rover", "Saab", "Saleen", "Saturn", "Scion", "SEAT", "Shelby", "Škoda",
    "Smart", "Spyker", "SsangYong", "Subaru", "Suzuki", "Talbot", "Tata", "Tatra", "Tesla", "Toyota",
    "Trabant", "Triumph", "TVR", "Vauxhall", "Vector", "Venturi", "Volkswagen", "Volvo", "Wartburg",
    "Westfield", "Wiesmann", "Zastava", "ZAZ", "Zenvo", "Zimmer",
]

# Création des marques de voiture dans la base de données
for nom in MARQUES:
    Marque.objects.create(nom=nom)
