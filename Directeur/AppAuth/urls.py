from django.urls import path
from .views import *

urlpatterns = [
    path('', AuthViews.as_view(), name='login'),
    path('', LogoutView.as_view(), name='logout'),
]