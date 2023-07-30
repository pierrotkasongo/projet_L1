from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from AppAdmin.models import *
from .models import *
from django.contrib import messages
from Election.config import generate_password
from django.core.mail import send_mail
from AppAuth.models import User
from Election import settings
from django.db.models import Q
from django.views import View
from django.dispatch import receiver
from django.db.models.signals import post_save
from AppEleve.models import Electeur
from django.db.models import Count

class ClasseView(View):
    def get(self, request):
        try:
            directeur = Directeur.objects.get(userId__id=request.user.id)
        except Directeur.DoesNotExist:
             return redirect('login')
        title = 'Classe' 
        return render(request, 'AppDirecteur/createReadClasse.html',
        {
            'title': title,
            'allClasse':Classe.objects.filter(ecoleId=directeur.ecoleId).order_by('classe')
        })

    def post(self, request):
        try:
            directeur = Directeur.objects.get(userId__id=request.user.id)
        except Directeur.DoesNotExist:
             return redirect('login')
        classe = request.POST.get('classe').lower()
        if not Classe.objects.filter(classe=classe, ecoleId=directeur.ecoleId):
            Classe.objects.create(classe=classe, ecoleId=directeur.ecoleId)
            messages.success(request, "Enregistremt réussi")
        else:
            messages.error(request, "La classe existe déjà!")
        return redirect('createReadClasse')

class UpdateClasseView(View):
    def get(self, request, id):
        try:
            directeur = Directeur.objects.get(userId__id=request.user.id)
        except Directeur.DoesNotExist:
             return redirect('login')
        objet = get_object_or_404(Classe, id=id)
        title = 'Classe'
        return render(request, 'AppDirecteur/updateClasse.html',
            {
                'title': title,
                'objet':objet,
                'allClasse': Classe.objects.filter(ecoleId=directeur.ecoleId).exclude(id=id).order_by('classe')
            })

    def post(self, request, id):
        objet = get_object_or_404(Classe, id=id)
        objet.classe = request.POST.get('classe').lower()
        objet.save()
        return redirect('createReadClasse')

class DeleteClasseView(View):
    def get(self, request, id):
        get_object_or_404(Classe, id=id).delete()
        return redirect('createReadClasse')

class EleveView(View):
    template_name = "AppDirecteur/createEleve.html" 
    title = 'Elèves'
    def get(self, request):
        try:
            directeur = Directeur.objects.get(userId__id=request.user.id)
        except Directeur.DoesNotExist:
             return redirect('login')
        allClasse = Classe.objects.filter(ecoleId=directeur.ecoleId).order_by('classe')
        allEleve = Eleve.objects.filter(classeId__ecoleId=directeur.ecoleId).order_by('classeId')
        return render(request, self.template_name, {
            'title': self.title,
            'allClasse':allClasse,
            'allEleve':allEleve
        })
        
    def post(self, request):
        nom = request.POST.get('nom').lower()
        postnom = request.POST.get('postnom').lower()
        prenom = request.POST.get('prenom').lower()
        email = request.POST.get('email').lower()
        email = request.POST.get('email').lower() 
        classe = int(request.POST.get('classe'))
        classeId = Classe.objects.get(id=classe)
        password = generate_password()
        if not User.objects.filter(email=email):
            user = User.objects.create_user(username=nom, first_name=postnom, last_name=prenom, email=email, password=password, status='eleve')
            Eleve.objects.create(userId=user, classeId=classeId)
            messages.success(request, "Enregistrement réussi")
        else:
            messages.error(request, "L'utilisateur existe deja !")
        return redirect('createEleve')

@receiver(post_save, sender=Eleve)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        user = instance.userId
        email = user.email
        password = generate_password()
        user.set_password(password)
        user.save()
        sujet = "Bienvenu dans Election app"
        message = "Votre adresse email : " + email + "\n" + "Votre mot de passe : " + password
        expediteur = settings.EMAIL_HOST_USER
        destinateur = [email]
        print(password, email)
        send_mail(sujet, message, expediteur, destinateur, fail_silently=True)

class UpdateEleveView(View):
    def get(self, request, id):
        objet = get_object_or_404(User, id=id)
        title = 'Modidication'
        try:
            directeur = Directeur.objects.get(userId__id=request.user.id)
        except Directeur.DoesNotExist:
             return redirect('login')
        allClasse = Classe.objects.filter(ecoleId=directeur.ecoleId).order_by('classe')
        return render(request, 'AppDirecteur/updateEleve.html', {
            'title':title,
            'objet':objet,
            'allClasse':allClasse
        })

    def post(self, request, id):
        objet = get_object_or_404(User, id=id)
        objet.username = request.POST.get('nom').lower()
        objet.first_name = request.POST.get('postnom').lower()
        objet.last_name =  request.POST.get('prenom').lower()
        objet.save()
        try:
            eleve = Eleve.objects.get(userId__id=id)
        except Eleve.DoesNotExist:
             return redirect('login')
        eleve.classeId = Classe.objects.get(id=int(request.POST.get('classe')))
        eleve.save()
        return redirect('readEleve')

class DeleteEleveView(View):
    def get(self, request, id):
        get_object_or_404(User, id=id).delete()
        return redirect('readEleve')

class ElectionView(View):
    def get(self, request):
        try:
            directeur = Directeur.objects.get(userId__id=request.user.id)
        except Directeur.DoesNotExist:
             return redirect('login')
        return render(request, "AppDirecteur/election.html",{
        'title':'Election',
        'election':Election.objects.filter(ecoleId=directeur.ecoleId, status='en cours')
    })
        
    def post(self, request):
        debut = request.POST.get('debut')
        fin = request.POST.get('fin')
        try:
            directeur = Directeur.objects.get(userId__id=request.user.id)
        except Directeur.DoesNotExist:
             return redirect('login')
        if debut < fin or debut == fin :
            if not Election.objects.filter(ecoleId=directeur.ecoleId, status='en cours'):
                Election.objects.create(ecoleId=directeur.ecoleId, dateDebut=debut, dateFin=fin)
                messages.success(request, "Election démarrer")
            else:
                messages.error(request, "Election en cours !")
        else:
            messages.error(request, "Dates incorrectes !")
        return redirect('election')

class ClotureElectionView(View):
    def get(self, request, id):
            objet = get_object_or_404(Election, id=id)
            objet.status = 'clôturer'
            objet.save()
            return redirect('election')

class CandidatView(View):
    def get(self, request):
        try:
            directeur = Directeur.objects.get(userId__id=request.user.id)
        except Directeur.DoesNotExist:
            return redirect('login')
        try:
            election = Election.objects.get(ecoleId=directeur.ecoleId, status='en cours')
            allCandidat = Candidat.objects.filter(eleveId__classeId__ecoleId=directeur.ecoleId, electionId=election)
            boutonEnvoie = True
        except Election.DoesNotExist:
            boutonEnvoie = False
            allCandidat = []
        return render(request, "AppDirecteur/createReadCandidat.html", {
            'title':'Candidats',
            'allEleve':  Eleve.objects.filter(classeId__ecoleId=directeur.ecoleId).exclude(candidat__electionId__status='en cours'),
            'allCandidat': allCandidat,
            'boutonEnvoie':boutonEnvoie
        })
         
    def post(self, request):
        try:
            directeur = Directeur.objects.get(userId__id=request.user.id)
        except Directeur.DoesNotExist:
            return redirect('login')
        try:
            election = Election.objects.get(ecoleId=directeur.ecoleId, status='en cours')
        except Election.DoesNotExist:
            return redirect('login')
        eleve = int(request.POST.get('candidat'))
        try:
            eleveId = Eleve.objects.get(userId__id=eleve)
        except Eleve.DoesNotExist:
            return redirect('login')
        Candidat.objects.create(eleveId=eleveId, electionId=election)
        messages.success(request, "Enregistrement réussi")
        return redirect('createReadCandidat')

class DeleteCandidat(View):
    def get(self, request, id):
        try:
            directeur = Directeur.objects.get(userId__id=request.user.id)
        except Directeur.DoesNotExist:
            return redirect('login')
        
        try:
            election = Election.objects.get(ecoleId=directeur.ecoleId, status='en cours')
        except Election.DoesNotExist:
            return redirect('login')
        
        Candidat.objects.get(eleveId=id, electionId=election).delete()
        return redirect('createReadCandidat')

class ResultatView(View):
    def get(self, request):
        try:
            directeur = Directeur.objects.get(userId__id=request.user.id)
        except Directeur.DoesNotExist:
            return redirect('login')
        election = Election.objects.filter(ecoleId=directeur.ecoleId, status='clôturer')
        if not election :
            resultat = False
        else :
            resultat = True
        return render(request, "AppDirecteur/resultat.html", {
            'title':'Résultat',
            'election':election,
            'resultat':resultat
        })

class DetailResultView(View):
    def get(self, request, id):
        try:
            directeur = Directeur.objects.get(userId__id=request.user.id)
        except Directeur.DoesNotExist:
            return redirect('login')
        voix = Electeur.objects.filter(electionId=id, electionId__ecoleId=directeur.ecoleId).values(
            'candidatId__eleveId__userId__username', 
            'candidatId__eleveId__userId__first_name', 
            'candidatId__eleveId__userId__last_name', 'eleveId__classeId__classe').annotate(count=Count('candidatId')).order_by('eleveId__classeId__classe')
        print(voix)
        return render(request, "AppDirecteur/voix.html", {
            'voix':voix,
        })