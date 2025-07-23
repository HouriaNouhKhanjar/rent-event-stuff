from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_supplies, name="supplies"),
    path('<int:supply_id>/', views.supply_detail, name="supply_detail"),
    path('add_supply', views.manage_supply, name='add_supply'),
    path('edit_supply/<int:supply_id>/', views.manage_supply, name='edit_supply'),
]
