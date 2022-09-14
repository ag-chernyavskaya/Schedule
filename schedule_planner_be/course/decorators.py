def permitted_user(view):
    def wrapper_func(request, *args, **kwargs):
        if request.user.role == "Super Admin":
            return view(request, *args, **kwargs)
        else:
            raise PermissionError("Only Super Admin has permission to do it.")

    return wrapper_func
