from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Election.config import generate_password
from Election import settings
from django.core.mail import send_mail
from AppAuth.models import User
from django.views import View
from django.dispatch import receiver
from django.db.models.signals import post_save



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
        postnom = request.POST.get('postnom').lower()
        prenom = request.POST.get('prenom').lower()
        email = request.POST.get('email').lower() 
        ecole = int(request.POST.get('ecole'))
        ecoleId = Ecole.objects.get(id=ecole)
        password = generate_password()
        if not User.objects.filter(email=email):
            user = User.objects.create_user(username=nom, first_name=postnom, last_name=prenom, email=email, password=password, status='directeur')
            Directeur.objects.create(userId=user, ecoleId=ecoleId)
            messages.success(request, "Enregistrement réussi")
        else:
            messages.error(request, "L'utilisateur existe deja !")
        return redirect('createDirecteur')

@receiver(post_save, sender=Directeur)
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
        send_mail(sujet, message, expediteur, destinateur, fail_silently=True)

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