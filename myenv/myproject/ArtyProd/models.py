from django.contrib.auth.models import  User
from django.db import models
from customer.models import Customer

class Service(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField()
    CATEGORIE_CHOICES = (
        ('CG', 'Charte graphique'),
        ('O3D', 'Objet 3D'),
        ('SC', 'Scénarisation'),
    )
    categorie = models.CharField(max_length=3, choices=CATEGORIE_CHOICES)
    img = models.ImageField(blank=True,upload_to='media/')

    def __str__(self):
        return self.nom

class Projet(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField()
    client = models.CharField(max_length=200)
    date_debut = models.DateField()
    date_fin = models.DateField()
    services = models.ManyToManyField(Service, through='Detail')
    equipe = models.ForeignKey('Equipe', on_delete=models.SET_NULL, null=True, blank=True)
    fichier = models.FileField(blank=True, upload_to='media/')
    customer= models.ForeignKey(Customer, on_delete=models.CASCADE)
    def __str__(self):
        return self.nom

class Detail(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)
    fichier = models.FileField(upload_to='media/')

    def __str__(self):
        return f"{self.service.nom} - {self.projet.nom}"


class Equipe(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.nom

class Personnel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE, related_name='personnel')
    poste = models.CharField(max_length=200)
    img = models.ImageField(blank=True, upload_to='media/')

    def __str__(self):
        return self.user.username

class Client(models.Model):
    nom = models.CharField(max_length=200)
    email = models.EmailField()
    telephone = models.CharField(max_length=20, blank=True)
    est_enregistre = models.BooleanField(default=False)
    admin = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    logo = models.ImageField(blank=True, upload_to='media/')

    def __str__(self):
        return self.nom

class Tache(models.Model):
    nom = models.CharField(max_length=200)
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, related_name='taches')
    description = models.TextField(blank=True)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='taches')
    date_debut = models.DateField()
    date_fin = models.DateField()
    assignee_a = models.ManyToManyField(Personnel, blank=True, related_name='assigned_taches')
    completee = models.BooleanField(default=False)

    def __str__(self):
        return self.nom






class Question(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.CASCADE)
    description =models.CharField(max_length=500)
    admin_comment=models.CharField(max_length=200,default='Nothing')
    asked_date =models.DateField(auto_now=True)
    def __str__(self):
        return self.description
    

