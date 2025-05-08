from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_car, name='add_car'),
    path('edit/<int:pk>/', views.edit_car, name='edit_car'),
    path('delete/<int:pk>/', views.delete_car, name='delete_car'),
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
    path('cars/', views.car_list, name='car_list'),
    
    # info pages
    path('faq/', views.faq, name='faq'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('latest/', views.latest, name='latest'),
]