def get_username(request):
    if request.user.is_authenticated:
        user_name = request.user.username
    else:
        user_name = None
    return user_name
#if user will change the name