from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import SecureLoginForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = SecureLoginForm(request, data=request.POST)
        if form.is_valid():
            request.session.flush()

            user = form.get_user()
            login(request, user)

            return redirect('dashboard')
        else:
            messages.error(request,"Email ou mot de passe incorrect. Votre compte pourrait être temporairement verrouillé.")
    else:
        form = SecureLoginForm()
    return render(request, 'accounts/login.html', {'form': form})