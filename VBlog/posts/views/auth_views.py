from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from posts.forms.auth_form import *


class SignUpController(View):

    def get(self, request):
        form = SignUpForm()
        context = {
            'form': form,
            'title': 'Sign Up | OnlineApp'
        }
        return render(request=request, template_name='signup.html', context=context)

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            user = authenticate(request=request, username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('posts:list')
            else:
                messages.error(request, "Invalid Credentials entered! Please try again!")

            return render(request=request, template_name='signup.html', context={'form': form})


class LoginController(View):

    def get(self, request):

        if request.user.is_authenticated:
            return redirect('posts:list')

        login_form = LoginForm
        context = {
            'form': login_form,
            'title': 'Login | OnlineApp'
        }
        return render(request=request, template_name="login.html", context=context)

    def post(self, request, *args, **kwargs):

        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user = authenticate(request=request, username=login_form.cleaned_data['username'],
                                password=login_form.cleaned_data['password'])

            if user is not None:
                login(request, user)
                return redirect('posts:list')
            else:
                messages.error(request, "Invalid Credentials entered! Please try again!")
                return redirect('login')


def logout_user(request):
    logout(request)
    return redirect('login')

