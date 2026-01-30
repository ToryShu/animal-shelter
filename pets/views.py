from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.admin.views.decorators import staff_member_required
from .models import Animal, AdoptionRequest, ShelterSettings
from .forms import AdoptionRequestForm, UserLoginForm, UserRegisterForm, ShelterSettingsForm, AnimalForm
from .decorators import admin_required

User = get_user_model()



def manage_animals(request):
    animals = Animal.objects.all()
    return render(request, "pets/admin/dashboard.html", {
        "animals": animals
    })


def animal_list(request):
    animal_type = request.GET.get('type')

    if animal_type == 'cat':
        animals = Animal.objects.filter(species='cat')
    elif animal_type == 'dog':
        animals = Animal.objects.filter(species='dog')
    else:
        animals = Animal.objects.all()

    return render(request, 'pets/public/animal_list.html', {
        'animals': animals,
        'animal_type': animal_type
    })



@login_required
def animal_detail(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    return render(request, 'pets/public/animal_detail.html', {'animal': animal})


@login_required
def adopt_animal(request, pk):
    animal = get_object_or_404(Animal, pk=pk)

    if request.method == "POST":
        message = request.POST.get("message")
        AdoptionRequest.objects.create(
            user=request.user,
            animal=animal,
            message=message
        )
        return redirect('pets:animal_list')
    return render(request, 'pets/adopt_form.html', {'animal': animal})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('pets:animal_list')
    else:
        form = UserLoginForm()

    return render(request, 'pets/public/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('pets:animal_list')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('pets:login')
    else:
        form = UserRegisterForm()

    return render(request, 'pets/public/register.html', {'form': form})


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
    animals = Animal.objects.all()
    total_animals = animals.count()
    available_animals = animals.filter(adopted=False).count()
    adopted_animals = animals.filter(adopted=True).count()

    context = {
        'animals': animals,
        'total_animals': total_animals,
        'available_animals': available_animals,
        'adopted_animals': adopted_animals,
    }

    return render(request, 'pets/admin/animals.html', context)



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
    adoption_requests = AdoptionRequest.objects.select_related("animal", "user").order_by("-created_at")
    return render(request, 'pets/admin/requests.html', {'adoption_requests': adoption_requests})

@admin_required
def admin_users(request):
    users = User.objects.all()
    return render(request, "pets/admin/users.html", {"users": users})


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
            messages.success(request, "Shelter settings updated!")
            return redirect('pets:admin_dashboard')
    else:
        form = ShelterSettingsForm(instance=settings)

    return render(request, 'pets/admin/settings.html', {'form': form})

def request_success(request, animal_id):
    animal = Animal.objects.get(id=animal_id)
    gif_url_postid = "11748501437476694103" if animal.species.lower() == 'cat' else "24314518"
    return render(request, "pets/admin/request_result.html", {
        "animal": animal,
        "gif_url": f"https://tenor.com/view/{gif_url_postid}",
        "status": "approved"
    })

def request_rejected(request, animal_id):
    animal = Animal.objects.get(id=animal_id)
    gif_url_postid = "12756433236776117962" if animal.species.lower() == 'cat' else "18089551" 
    return render(request, "pets/admin/request_result.html", {
        "animal": animal,
        "gif_url": f"https://tenor.com/view/{gif_url_postid}",
        "status": "rejected"
    })

def landing(request):
    return render(request, 'pets/public/landing.html')

@login_required
def my_adoption_requests(request):
    adoption_requests = AdoptionRequest.objects.filter(user=request.user).select_related("animal").order_by("-created_at")
    return render(request, 'pets/public/my_requests.html', {'adoption_requests': adoption_requests})

