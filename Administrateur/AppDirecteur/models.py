from django.db import models
from AppAdmin.models import *

class Classe(models.Model):
    ecoleId = models.ForeignKey(Ecole, on_delete=models.CASCADE)
    classe = models.CharField(max_length=100)

    def __str__(self):
        return self.classe

class Eleve(models.Model):
    userId = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    classeId = models.ForeignKey(Classe, on_delete=models.CASCADE)

    def __str__(self):
        return self.userId.username
    
class Election(models.Model):
    ecoleId = models.ForeignKey(Ecole, on_delete=models.CASCADE)
    dateDebut = models.DateField()
    dateFin = models.DateField()
    status = models.CharField(max_length=50, default='en cours')

    def __str__(self):
        return self.ecoleId.ecole + " : " + self.status
    
class Candidat(models.Model):
    eleveId = models.ForeignKey(Eleve, on_delete=models.CASCADE)
    electionId = models.ForeignKey(Election, on_delete=models.CASCADE)
   
    def __str__(self):
        return self.eleveId.userId.username