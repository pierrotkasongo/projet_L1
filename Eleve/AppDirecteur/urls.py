from django.urls import path
from .views import *

urlpatterns = [
    path('createReadClasse', ClasseView.as_view(), name='createReadClasse'),
    path('updateClasse/<int:id>', UpdateClasseView.as_view(), name='updateClasse'),
    path('deleteClasse/<int:id>', DeleteClasseView.as_view(), name='deleteClasse'),
    path('createEleve', EleveView.as_view(), name='createEleve'),
    path('readEleve', EleveView.as_view(template_name="AppDirecteur/readEleve.html", title="Liste des élèves"), name='readEleve'),
    path('updateEleve/<int:id>', UpdateEleveView.as_view(), name='updateEleve'),
    path('deleteEleve/<int:id>', DeleteEleveView.as_view(), name='deleteEleve'),
    path('election', ElectionView.as_view(), name='election'),
    path('cloturerElection/<int:id>', ClotureElectionView.as_view(), name='cloturerElection'),
    path('createReadCandidat', CandidatView.as_view(), name='createReadCandidat'),
    path('deleteCandidat/<int:id>', DeleteCandidat.as_view(), name='deleteCandidat'),
    path('resultat', ResultatView.as_view(), name='resultat'),
    path('voix/<int:id>', DetailResultView.as_view(), name='voix'),
]
