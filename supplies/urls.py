from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_supplies, name="supplies"),
    path('<supply_id>', views.supply_detail, name="supply_detail"),
]
