from django.urls import path
from .views import *

urlpatterns = [
    path('home', HomeView.as_view(), name='home'),
    path('createReadEcole', EcoleView.as_view(), name='createReadEcole'),
    path('updateEcole/<int:id>', UpdateEcoleView.as_view(), name='updateEcole'),
    path('deleteEcole/<int:id>', DeleteEcoleView.as_view(), name='deleteEcole'),
    path('createDirecteur', DirecteurView.as_view(), name='createDirecteur'),
    path('readDirecteur', DirecteurView.as_view(template_name='AppAdmin/readDirecteur.html', title='Liste Directeur'), name='readDirecteur'),
    path('deleteDirecteur/<int:id>', DeleteDirecteurView.as_view(), name='deleteDirecteur'),
    path('updateDirecteur/<int:id>', UpdateDirecteurView.as_view(), name='updateDirecteur'),
]