from django.db import models
# Create your models here.
from AppAuth.models import User

class Ecole(models.Model):
    ecole = models.CharField(max_length=200)

    def __str__(self):
        return self.ecole

class Directeur(models.Model):
    userId = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    ecoleId = models.ForeignKey(Ecole, on_delete=models.CASCADE)

    def __str__(self):
        return self.userId.username