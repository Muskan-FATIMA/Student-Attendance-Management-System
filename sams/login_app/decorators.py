from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group == 'teacher':
                return redirect('teacher_profile')
            elif group == 'admin':
                return redirect('admin_profile')
        return view_func(request, *args, **kwargs)
    return wrapper_func