from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Administrateur.config import generate_password
from Administrateur import settings
from django.core.mail import send_mail
from AppAuth.models import User
from AppDirecteur.models import *
from AppEleve.models import *
from django.views import View
from django.dispatch import receiver
from django.db.models.signals import post_save
from .producer import *

from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, '')

class HomeView(View):
    def get(self, request):
        title = 'Home'
        now = datetime.today().strftime('%A %d %B %Y, %H:%M')
        directeursNum = Directeur.objects.count()
        ecoleNum = Ecole.objects.count()
        eleveNum = Eleve.objects.count()
        candidatNum = Candidat.objects.count()
        classeNum = Classe.objects.count()
        electionNum = Election.objects.count()
        electeurNum = Electeur.objects.count()
        return render(request,  'AppAdmin/home.html', 
            {
                'title':title,
                'now': now,
                'directeursNum':directeursNum,
                'ecoleNum':ecoleNum,
                'eleveNum':eleveNum,
                'candidatNum':candidatNum,
                'classeNum':classeNum,
                'electionNum':electionNum,
                'electeurNum':electeurNum
            })

class EcoleView(View):
    def get(self, request):
        title = 'Ecole'
        allEcole = Ecole.objects.all().order_by('ecole')
        return render(request,  'AppAdmin/createReadEcole.html', 
            {
                'title':title,
                'allEcole':allEcole
            })

    def post(self, request):
        ecole = request.POST.get('ecole').lower()
        if not Ecole.objects.filter(ecole=ecole):
            Ecole.objects.create(ecole=ecole)
            message =f"ecole: {ecole}"
            publish_message('ecoles', message)
            publish_message('elevecoles', message)
            messages.success(request, "Enregistrement réussi")
        else:
            messages.error(request, "L'ecole existe deja !")
        return redirect('createReadEcole')

class UpdateEcoleView(View):
    def get(self, request, id):
        title = 'Ecole'
        objet = get_object_or_404(Ecole, id=id)
        allEcole = Ecole.objects.exclude(id=id).order_by('ecole')
        return render(request, 'AppAdmin/updateEcole.html', 
            {
                'title':title,
                'objet':objet,
                'allEcole': allEcole
            })

    def post(self, request, id):
        objet = get_object_or_404(Ecole, id=id)
        objet.ecole = request.POST.get('ecole').lower()
        objet.save()
        return redirect('createReadEcole')

class DeleteEcoleView(View):
    def get(self, request, id):
        get_object_or_404(Ecole, id=id).delete()
        return redirect('createReadEcole')

class DirecteurView(View):
    template_name = "AppAdmin/createDirecteur.html" 
    title = 'Directeur'
    def get(self, request):
        return render(request, self.template_name, 
        {
            'title': self.title,
            'allEcole':Ecole.objects.all(),
            'allDirecteur' :Directeur.objects.all()
        })

    def post(self, request):
        nom = request.POST.get('nom').lower()
        potsnom = request.POST.get('postnom').lower()
        prenom = request.POST.get('prenom').lower()
        email = request.POST.get('email').lower() 
        ecole = int(request.POST.get('ecole'))
        ecoleId = Ecole.objects.get(id=ecole)
        password = generate_password()
        print("views generer",password)
        if not User.objects.filter(email=email):
            user = User.objects.create_user(username=nom, first_name=potsnom, last_name=prenom, email=email, password=password, status='directeur')
            Directeur.objects.create(userId=user, ecoleId=ecoleId)
            
            name_ecole = ecoleId.ecole        
            message =f"nom: {nom}, potsnom: {potsnom}, prenom: {prenom}, email: {email}, password: {password}, ecole: {name_ecole}"
            print(message)
            publish_message('directeurs', message)
            publish_message('elevedirecteurs', message)
            
            sujet = "Bienvenu dans Election app"
            message = "Votre adresse email : " + email + "\n" + "Votre mot de passe : " + password
            expediteur = settings.EMAIL_HOST_USER
            destinateur = [email]
            send_mail(sujet, message, expediteur, destinateur, fail_silently=True)
            
            messages.success(request, "Enregistrement réussi")
        else:
            messages.error(request, "L'utilisateur existe deja !")
        return redirect('createDirecteur')

class UpdateDirecteurView(View):
    def get(self, request, id):
        objet = get_object_or_404(User, id=id)
        title = 'Modidication'
        return render(request, 'AppAdmin/updateDirecteur.html', {
            'title':title,
            'objet':objet,
            'allEcole':Ecole.objects.all()
        })

    def post(self, request, id):
        objet = get_object_or_404(User, id=id)
        objet.username = request.POST.get('nom').lower()
        objet.first_name = request.POST.get('postnom').lower()
        objet.last_name =  request.POST.get('prenom').lower()
        objet.save()
        try:
            directeur = Directeur.objects.get(userId__id=id)
        except Directeur.DoesNotExist:
             return redirect('login')
        directeur.ecoleId = Ecole.objects.get(id=int(request.POST.get('ecole')))
        directeur.save()
        return redirect('readDirecteur')

class DeleteDirecteurView(View):
    def get(self, request, id):
        get_object_or_404(User, id=id).delete()
        return redirect('readDirecteur')
    
