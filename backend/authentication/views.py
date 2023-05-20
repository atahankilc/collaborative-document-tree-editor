from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from .forms import LoginForm, SignUpForm

import sys

sys.path.append("..")
from client.ClientHandler import ClientHandler


class Login(View):
    @staticmethod
    def get(request):
        if ('token' in request.COOKIES) or (not request.session.exists(request.session.session_key)):
            return redirect('home')

        form = LoginForm()
        return render(request, 'authentication/login.html', {'form': form})

    @staticmethod
    def post(request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            client = ClientHandler.get_session(request.session.session_key)
            client.add_to_sending_queue(f'login {username} {password}')
            response = client.pop_from_receiving_queue()

            if response.startswith('token:'):
                token = response.split()[1]
                response = redirect('home')
                response.set_cookie('token', token)
                messages.success(request, 'You are now logged in.')
                return response
            else:
                messages.error(request, response)
                return redirect('login')


class SignUp(View):
    @staticmethod
    def get(request):
        if ('token' in request.COOKIES) or (not request.session.exists(request.session.session_key)):
            return redirect('home')

        form = SignUpForm()
        return render(request, 'authentication/signup.html', {'form': form})

    @staticmethod
    def post(request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            fullname = form.cleaned_data['fullname']
            password = form.cleaned_data['password']

            client = ClientHandler.get_session(request.session.session_key)
            client.add_to_sending_queue(f'signup {username} {email} {fullname} {password}')
            response = client.pop_from_receiving_queue()

            if response.startswith('token:'):
                token = response.split()[1]
                response = redirect('home')
                response.set_cookie('token', token)
                messages.success(request, 'You are now registered.')
                return response
            else:
                messages.error(request, response)
                return redirect('signup')


class Logout(View):
    @staticmethod
    def get(request):
        if ('token' not in request.COOKIES) or (not request.session.exists(request.session.session_key)):
            return redirect('home')

        client = ClientHandler.get_session(request.session.session_key)
        client.add_to_sending_queue(f'logout')
        messages.success(request, client.pop_from_receiving_queue())
        response = redirect('home')
        response.delete_cookie("token")
        return response
