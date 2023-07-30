from django.db import models
from AppDirecteur.models import Eleve, Election, Candidat

class Electeur(models.Model):
    eleveId = models.ForeignKey(Eleve, on_delete=models.CASCADE)
    electionId = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidatId = models.ForeignKey(Candidat, on_delete=models.CASCADE)

    def __str__(self):
        return self.candidatId.eleveId.userId.username