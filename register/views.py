from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from .forms import SignUpForm, UpdateUserProfileForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class DeleteProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user_instance = get_object_or_404(CustomUser, pk=request.user.id)
        return render(request, "registration/delete.html", {"user": user_instance})

    def post(self, request):
        user_instance = get_object_or_404(CustomUser, pk=request.user.id)
        if user_instance == request.user:
            user_instance.delete()
            return redirect("login")
        else:
            return render(request, "registration/login.html")


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        context = {"user": user}
        return render(request, "profile.html", context=context)


class UpdateProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = UpdateUserProfileForm(instance=request.user)
        context = {"form": form}
        return render(request, "registration/update_profile.html", context)

    def post(self, request):
        form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")


class CustomUserSignup(View):
    def get(self, request):
        form = SignUpForm()
        context = {
            "form": form,
        }
        return render(request, "registration/signup.html", context)

    def post(self, request):
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")

        context = {
            "form": form,
        }
        return render(request, "registration/signup.html", context)


class CustomUserLogin(View):
    def get(self, request):
        form = AuthenticationForm()
        context = {
            "form": form,
        }
        return render(request, "registration/login.html", context)

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
        else:
            return render(request, "registration/login.html", {"form": form})


class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")
