from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('update_profile_address/<address_type>', views.update_address,
         name='update_address'),
]
