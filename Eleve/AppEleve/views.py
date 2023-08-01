from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from AppDirecteur.models import Eleve, Candidat, Election
from .models import Electeur
from django.views import View
from django.db.models import Count
from .producer import *

class VoteView(View):
    def get(self, request):
        try:
            eleve = Eleve.objects.get(userId=request.user.id)
        except Eleve.DoesNotExist:
            return redirect('login')
        try:
            election = Election.objects.get(ecoleId=eleve.classeId.ecoleId, status='en cours')
            demarrerElection = True
            vote = Electeur.objects.filter(electionId=election, eleveId=eleve).exists()     
        except Election.DoesNotExist:
            demarrerElection = False
            vote = False
        return render(request, "AppEleve/vote.html", {
            'title':'Vote',
            'demarrerElection': demarrerElection,
            'vote':vote,
            'allCandidat':Candidat.objects.filter(eleveId__classeId=eleve.classeId, electionId__status='en cours').order_by('eleveId__userId__username'),
        })


# class ElecteurView(View):
#     def get(self, request, id):
#         try:
#             eleve = Eleve.objects.get(userId=request.user.id)
#         except Eleve.DoesNotExist:
#             return redirect('login')
#         try:
#             election = Election.objects.get(ecoleId=eleve.classeId.ecoleId, status='en cours')
#         except Election.DoesNotExist:
#             return redirect('login')
#         #Electeur.objects.create(electionId=election, eleveId=eleve, candidatId=get_object_or_404(Candidat, eleveId__userId__id=id))
#         message = f"eleve:{eleveId.userId.username},election:{election.ecoleId.ecole}, candidat:{candidat.eleveId.userId.username}"
#         print(message)
        
#         return redirect('vote')


class ElecteurView(View):
    def get(self, request, id):
        try:
            eleve = Eleve.objects.get(userId=request.user.id)
        except Eleve.DoesNotExist:
            return redirect('login')
        try:
            election = Election.objects.get(ecoleId=eleve.classeId.ecoleId, status='en cours')
        except Election.DoesNotExist:
            return redirect('login')
            
        candidat = get_object_or_404(Candidat, eleveId__userId__id=id)
        Electeur.objects.create(electionId=election, eleveId=eleve, candidatId=candidat)
        
        message = f"eleve:{eleve.userId.username},election:{election.ecoleId.ecole},candidat:{candidat.eleveId.userId.username}"
        print(message)
        publish_message('electeurs', message)
        publish_message('electeursdirecteurs', message)
        
        return redirect('vote')






class EleveResultatView(View):
    def get(self, request):
        try:
            eleve = Eleve.objects.get(userId=request.user.id)
        except Eleve.DoesNotExist:
            return redirect('login')
        election = Election.objects.filter(ecoleId=eleve.classeId.ecoleId, status='clôturer')
        if not election :
            resultat = False
        else :
            resultat = True
        return render(request, "AppEleve/resultat.html", {
            'title':'Résultat',
            'election':election,
            'resultat':resultat
        })

class EleveDetailResultView(View):
    def get(self, request, id):
        try:
            eleve = Eleve.objects.get(userId=request.user.id)
        except Eleve.DoesNotExist:
            return redirect('login')
        voix = Electeur.objects.filter(electionId=id, eleveId__classeId=eleve.classeId).values(
            'candidatId__eleveId__userId__username', 
            'candidatId__eleveId__userId__first_name', 
            'candidatId__eleveId__userId__last_name').annotate(count=Count('candidatId'))
        print(voix)
        return render(request, "AppEleve/voix.html", {
            'voix':voix,
        })