# decorators.py
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión primero.')
            return redirect('vetweb:login')
        
        if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'ADMIN':
            messages.error(request, 'No tienes permisos para acceder a esta sección.')
            return redirect('vetweb:index')
        
        return view_func(request, *args, **kwargs)
    return wrapper