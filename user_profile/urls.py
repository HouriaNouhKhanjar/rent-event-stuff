from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('update_profile_address', views.update_address,
         name='update_address'),
]
