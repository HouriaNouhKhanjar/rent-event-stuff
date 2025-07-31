from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('update_profile_address/', views.update_address,
         name='update_address'),
    path('order_history/<order_number>/', views.order_history,
         name='order_history'),
    path('save_supply/<int:supply_id>/', views.toggle_save_supply,
         name='toggle_save_supply'),

]
