from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You need to login first.')
            return redirect('pets:login')
        
        if not request.user.is_admin and not request.user.is_superuser:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('pets:animal_list')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper
