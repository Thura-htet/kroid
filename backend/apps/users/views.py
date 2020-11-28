from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def login_view(request, *args, **kwargs):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('/')
    context = {
        "form": form,
        "btn_label": "Login",
        "title": "Login"
    }
    return render(request, 'users/auth.html', context, status=200)


def logout_view(request, *args, **kwargs):
    if request.method == "POST":
        logout(request)
        return redirect("/auth/login/")
    context = {
        "form": None,
        "btn_label": "Click to confirm",
        "title": "Logout"
    }
    return render(request, "users/auth.html", context, status=200)


def resgister_view(request, *args, **kwargs):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=True)
        user.set_password(form.clean_password2)
        login(request, user)
        return redirect('/auth/login/')
    context = {
        "form": form,
        "btn_label": "Register",
        "title": "Register"
    }
    return render(request, "users/auth.html", context, status=200)