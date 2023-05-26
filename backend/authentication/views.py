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
        if ('token' in request.COOKIES) or \
                ('documentid' in request.COOKIES) or \
                (request.session.session_key not in ClientHandler.client_dict):
            return redirect('home')

        form = LoginForm()
        return render(request, 'authentication/login.html', {'form': form})

    @staticmethod
    def post(request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            command = f'login {username} {password}'
            ClientHandler.send_to_session(request.session.session_key, command)
            response = ClientHandler.receive_from_session(request.session.session_key, '')

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
        if ('token' in request.COOKIES) or \
                ('documentid' in request.COOKIES) or \
                (request.session.session_key not in ClientHandler.client_dict):
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

            command = f'signup {username} {email} {fullname} {password}'
            ClientHandler.send_to_session(request.session.session_key, command)
            response = ClientHandler.receive_from_session(request.session.session_key, '')

            if response.startswith('token:'):
                token = response.split()[1]
                response = redirect('home')
                response.set_cookie('token', token)
                messages.success(request, 'You are now registered.')
                return response
            else:
                messages.error(request, response)
                return redirect('signup')
        messages.error(request, 'Invalid Form')
        return redirect('signup')


class Logout(View):
    @staticmethod
    def get(request):
        if ('token' not in request.COOKIES) or \
                ('documentid' in request.COOKIES) or \
                (request.session.session_key not in ClientHandler.client_dict):
            return redirect('home')

        ClientHandler.send_to_session(request.session.session_key, 'logout', request.COOKIES["token"])
        response = ClientHandler.receive_from_session(request.session.session_key, '')

        messages.success(request, response)
        response = redirect('home')
        response.delete_cookie("token")
        return response
