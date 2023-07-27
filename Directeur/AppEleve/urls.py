from django.urls import path
from .views import *

urlpatterns = [
    path('vote', VoteView.as_view(), name='vote'),
    path('electeur/<int:id>', ElecteurView.as_view(), name='electeur'),
    path('resultatEleve', EleveResultatView.as_view(), name='resultatEleve'),
    path('eleveVoix/<int:id>', EleveDetailResultView.as_view(), name='eleveVoix'),
]
