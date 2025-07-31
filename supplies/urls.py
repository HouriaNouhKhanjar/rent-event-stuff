from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_supplies, name="supplies"),
    path('<int:supply_id>/', views.supply_detail, name="supply_detail"),
    path('add_supply', views.add_supply, name='add_supply'),
    path('edit_supply/<int:supply_id>/', views.edit_supply,
         name='edit_supply'),
    path('supply-delete/<int:pk>/', views.delete_supply,
         name='delete_supply'),
    path('image/<int:pk>/delete/', views.delete_supply_image,
         name='delete_supply_image'),
    path('review_supply/<int:supply_id>/', views.review_supply,
         name='review_supply'),
]
