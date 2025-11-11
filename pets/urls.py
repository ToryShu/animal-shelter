from django.urls import path
from . import views
from django.shortcuts import render, get_object_or_404
from .models import Animal

app_name = 'pets'

urlpatterns = [
    path('', views.animal_list, name='animal_list'),
    path('animal/<int:pk>/', views.animal_detail, name='animal_detail'),
    path('animal/<int:pk>/adopt/', views.adopt_animal, name='adopt_animal'),
]

def animal_list(request):
    animals = Animal.objects.order_by('-created_at')
    return render(request, 'pets/animal_list.html', {'animals': animals})

def animal_detail(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    return render(request, 'pets/animal_detail.html', {'animal': animal})

urlpatterns = [
    path('', views.animal_list, name='animal_list'),
    path('animal/<int:pk>/', views.animal_detail, name='animal_detail'),
    path('animal/<int:pk>/adopt/', views.adopt_animal, name='adopt_animal'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
]
