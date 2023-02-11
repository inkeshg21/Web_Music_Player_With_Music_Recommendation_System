from django.shortcuts import redirect


def unauthenticated_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_function(request, *args, **kwargs)

    return wrapper_function


def admin_only(view_function):
    def wrapper_function(request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('/')
        else:
            return view_function(request, *args, **kwargs)

    return wrapper_function


def user_only(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_superuser:
            return redirect('/admins')
        else:
            return view_function(request, *args, **kwargs)

    return wrapper_function