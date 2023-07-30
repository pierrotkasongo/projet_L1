from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View

class AuthViews(View):
    def get(self, request):
        return render(request, 'AppAuth/connexion.html', {'title': 'Connexion'})
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        
        if user is not None:
            login(request, user)
            if user.status == 'admin':
                return redirect('createReadEcole')
            elif user.status == 'directeur':
                return redirect('createReadClasse')
            elif user.status == 'eleve':
                return redirect('vote')

        messages.error(request, "Informations incorrectes")
        
        return render(request, 'AppAuth/connexion.html', {'title': 'Connexion'})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
