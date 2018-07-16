from registration.signals import user_registered, user_activated
from django.dispatch import receiver
from registration.forms import RegistrationFormUniqueEmail
from django.shortcuts import redirect
from django.contrib.auth import login

@receiver(user_registered)
def create(sender, user, request, **kwarg):
    user.refresh_from_db()  # load the profile instance created by the signal
    user.profile.CompanyContactEmail = request.POST.get('email')
    user.profile.CompanyID = user.profile.id
    user.email = user.profile.CompanyContactEmail
    user.save()

@receiver(user_activated)
def login_user(sender, user, request, **kwarg):
    """Logs in the user after activation"""
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')