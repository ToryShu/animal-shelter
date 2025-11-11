from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Animal, AdoptionRequest
from .forms import AdoptionRequestForm
from django.contrib.auth import login, authenticate, logout
from .forms import UserLoginForm
from .forms import UserRegisterForm

def animal_list(request):
    animals = Animal.objects.order_by('-created_at')
    return render(request, 'pets/animal_list.html', {'animals': animals})

def animal_detail(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    form = None
    if request.user.is_authenticated:
        form = AdoptionRequestForm()
    return render(request, 'pets/animal_detail.html', {'animal': animal, 'form': form})

@login_required
def adopt_animal(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    if animal.adopted:
        messages.error(request, 'This animal has already been adopted.')
        return redirect('pets:animal_detail', pk=pk)
    
    if request.method == 'POST':
        form = AdoptionRequestForm(request.POST)
        if form.is_valid():
            adoption = form.save(commit=False)
            adoption.user = request.user
            adoption.animal = animal
            adoption.save()
            messages.success(request, 'Your adoption request has been submitted!')
            return redirect('pets:animal_detail', pk=pk)
    else:
        form = AdoptionRequestForm()
    
    return render(request, 'pets/adopt_form.html', {'animal': animal, 'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('pets:animal_list')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('pets:animal_list')
    else:
        form = UserLoginForm()
    return render(request, 'pets/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('pets:animal_list')

def register(request):
    if request.user.is_authenticated:
        return redirect('pets:animal_list')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('pets:login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'pets/register.html', {'form': form})
