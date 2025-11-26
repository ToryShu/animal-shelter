from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserForm
from animals.views import admin_required

@admin_required
def user_list(request):
    users = User.objects.all().order_by('id')
    return render(request, 'adminpanel/user_list.html', {'users': users})

@admin_required
def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    form = UserForm(request.POST or None, instance=user)

    if form.is_valid():
        form.save()
        return redirect('user_list')

    return render(request, 'adminpanel/user_edit.html', {'form': form, 'user': user})

@admin_required
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        user.delete()
        return redirect('user_list')

    return render(request, 'adminpanel/user_delete.html', {'user': user})
