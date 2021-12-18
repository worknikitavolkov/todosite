from django.contrib.auth.decorators import user_passes_test

def check_user(user):
  return not user.is_authenticated

user_logout_required = user_passes_test(check_user,"/")

def auth_user_no_access(view):
  return user_logout_required(view)