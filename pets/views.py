from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Animal, AdoptionRequest, User
from .forms import AdoptionRequestForm
from django.contrib.auth import login, authenticate, logout
from .forms import UserLoginForm
from .forms import UserRegisterForm
from .decorators import admin_required
from .models import ShelterSettings
from pets.models import AdoptionRequest
from pets.decorators import admin_required
from .forms import ShelterSettingsForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .forms import AnimalForm



def animal_list(request):
    animal_type = request.GET.get('type')
    if animal_type in ['cat', 'dog']:
        animals = Animal.objects.filter(animal_type=animal_type, adopted=False)
    else:
        animals = Animal.objects.filter(adopted=False)

    return render(request, 'pets/animal_list.html', {
        'animals': animals,
        'selected_type': animal_type
    })


def animal_detail(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    return render(request, 'pets/animal_detail.html', {'animal': animal})

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

@admin_required
def admin_dashboard(request):
    context = {
        'total_animals': Animal.objects.count(),
        'available_animals': Animal.objects.filter(adopted=False).count(),
        'adopted_animals': Animal.objects.filter(adopted=True).count(),
        'pending_requests': 0,
        'total_users': 0,
    }
    return render(request, 'pets/admin/dashboard.html', context)


@staff_member_required
def admin_animals(request):
    animal_type = request.GET.get('type')
    if animal_type in ['cat', 'dog']:
        animals = Animal.objects.filter(animal_type=animal_type)
    else:
        animals = Animal.objects.all() 

    return render(request, 'pets/admin/animals.html', {'animals': animals, 'selected_type': animal_type})


@staff_member_required
def admin_animal_create(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Animal has been added!")
            return redirect('pets:admin_dashboard')
    else:
        form = AnimalForm()

    return render(request, 'pets/admin/animal_create.html', {'form': form})


@admin_required
def admin_animal_edit(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)
    form = AnimalForm(request.POST or None, request.FILES or None, instance=animal)
    if form.is_valid():
        form.save()
        messages.success(request, "Animal updated successfully!")
        return redirect('pets:admin_animals')
    return render(request, 'pets/admin/animal_edit.html', {'form': form, 'animal': animal})


@admin_required
def admin_animal_delete(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)
    if request.method == 'POST':
        animal.delete()
        messages.success(request, "Animal deleted successfully!")
        return redirect('pets:admin_animals')
    return render(request, 'pets/admin/animal_delete.html', {'animal': animal})


@admin_required
def admin_adoption_requests(request):
    adoption_requests = AdoptionRequest.objects.all()
    return render(request, 'pets/admin/requests.html', {'adoption_requests': adoption_requests})


def admin_users(request):
    return render(request, 'pets/admin/users.html')

def admin_settings(request):
    return render(request, 'pets/admin/settings.html')

@admin_required
def admin_requests_list(request):
    requests_list = AdoptionRequest.objects.select_related("animal", "user").order_by("-created_at")
    return render(request, "pets/admin/requests_list.html", {"requests": requests_list})


@admin_required
def admin_request_approve(request, pk):
    adoption_request = get_object_or_404(AdoptionRequest, pk=pk)
    adoption_request.status = 'approved'
    adoption_request.save()
    adoption_request.animal.status = 'Adopted'
    adoption_request.animal.save()
    return redirect("pets:request_success", animal_id=adoption_request.animal.id)


@admin_required
def admin_request_reject(request, pk):
    adoption_request = get_object_or_404(AdoptionRequest, pk=pk) 
    adoption_request.status = 'rejected'
    adoption_request.save()
    return redirect("pets:request_rejected", animal_id=adoption_request.animal.id)


@staff_member_required
def admin_settings(request):
    settings = ShelterSettings.objects.first()
    if not settings:
        settings = ShelterSettings.objects.create() 

    if request.method == 'POST':
        form = ShelterSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Shelter settings have been updated!")
            return redirect('pets:animal_list')
    else:
        form = ShelterSettingsForm(instance=settings)

    return render(request, 'pets/admin/settings.html', {'form': form})

def request_success(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)
    return render(request, "pets/admin/success.html", {"animal": animal})

def request_rejected(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)
    return render(request, "pets/admin/rejected.html", {"animal": animal})

def request_success(request, animal_id):
    animal = Animal.objects.get(id=animal_id)
    if animal.species.lower() == 'cat':
        gif_url_postid = "11748501437476694103"  # счастливый кот
    else:
        gif_url_postid = "24314518"  # счастливый пес
    return render(request, "pets/admin/request_result.html", {
        "animal": animal,
        "gif_url_postid": gif_url_postid,
        "gif_url": f"https://tenor.com/view/{gif_url_postid}",
        "status": "approved"
    })

def request_rejected(request, animal_id):
    animal = Animal.objects.get(id=animal_id)
    if animal.species.lower() == 'cat':
        gif_url_postid = "12756433236776117962"  # грустный кот
    else:
        gif_url_postid = "18089551"  # грустный пес
    return render(request, "pets/admin/request_result.html", {
        "animal": animal,
        "gif_url_postid": gif_url_postid,
        "gif_url": f"https://tenor.com/view/{gif_url_postid}",
        "status": "rejected"
    })
