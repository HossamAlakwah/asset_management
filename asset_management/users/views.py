from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import redirect, render

from .forms import CustomPasswordResetForm, CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


def is_super_admin(user):
    
    return user.is_authenticated and user.is_super_admin()

def is_admin(user):
    return user.is_authenticated and user.is_admin()


@user_passes_test(is_super_admin)
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} created successfully!')
            return redirect('create_user')
    else:
        form = CustomUserCreationForm(user=request.user)
    return render(request, 'create_user.html', {'form': form})

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_url = '/password_reset/done/'
    
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/assets/branches/')  # or wherever
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')
