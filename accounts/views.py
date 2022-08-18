from django.shortcuts import render
from .models import User
from django.views import View
from django import forms
from .forms import SignupForm, LoginForm, UserUpdateProfileForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login
from django.contrib.auth import authenticate
from accounts.mixins import IsSelfMixin
import re


# Create your views here.


class HomeView(LoginRequiredMixin, View):
    template_name = "accounts/home.html"

    def get(self, request):
        return render(request, self.template_name)


class SignupView(View):
    template_name = 'accounts/signup.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password2'])
            user.save()
            return redirect('accounts/login.html')
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    template_name = 'accounts/login.html'

    def get(self, request):
        form = LoginForm
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('courses:course_list')
        return render(request, self.template_name, {'message': 'Invalid username or password'})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login')


class UserUpdateProfile(IsSelfMixin, View):
    template_name = "accounts/profile_update.html"

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        form = UserUpdateProfileForm(instance=user)
        context = {
            "form": form
        }

        return render(request, self.template_name, context)

    def post(self, request, pk):
        user = User.objects.get(id=pk)
        form = UserUpdateProfileForm(
            request.POST, request.FILES, instance=user)
        if form.is_valid:
            print(form.data)
            form.save()
            return redirect('/')
        return render(request, self.template_name, {'form': form})


class UserProfileDetail(View):
    template_name = "accounts/profile_detail.html"
    model = User

    def get(self, request, pk):
        context = {
            "user": User.objects.get(id=pk)

        }
        return render(request, self.template_name, context=context)


class ChangePassword(View):
    template_name = "accounts/change_password.html"
    form_class = PasswordChangeForm

    def get(self, request):
        form = PasswordChangeForm
        context = {
            "form": form
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            password_confirmation = form.cleaned_data['password_confirmation']
            new_password = form.cleaned_data['new_password']

            if self.request.user.check_password(old_password):
                if new_password == password_confirmation:
                    # if len(new_password) < 8:
                    #     return render(request, self.template_name, {"form": form, "message": "password must have at least 8 character"})
                    # if re.findall("\D", new_password):
                    #     return render(request, self.template_name, {"form": form, "message": "password must have at least one number character "})
                    # if re.findall("[A-Z]", new_password):
                    #     return render(request, self.template_name, {"form": form, "message": "password must have at least one upper case"})
                    user = User.objects.get(id=request.user.id)
                    user.set_password(new_password)
                    user.save()
                    return render(request, self.template_name, {"form": form, "message": "Successfully!!"})
                return render(request, self.template_name, {"form": form, "message": "password donot match"})

            return render(request, self.template_name, {"form": form, "message": "please check your password"})
        return redirect('/')
