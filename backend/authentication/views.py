import pickle
import socket

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from .forms import LoginForm, SignUpForm

import sys

sys.path.append("..")
from client.ClientHandler import ClientHandler


# ClientHandler.client_dict


class Login(View):
    @staticmethod
    def get(request):
        if 'token' in request.COOKIES:
            return redirect('home')

        form = LoginForm()
        return render(request, 'authentication/login.html', {'form': form})

    @staticmethod
    def post(request):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(('localhost', 50001))
            pickle.loads(sock.recv(1024))
            sock.sendall(pickle.dumps('login'))
            pickle.loads(sock.recv(1024))

            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                sock.sendall(pickle.dumps(f'{username} {password}'))
                response = pickle.loads(sock.recv(1024))

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
        if 'token' in request.COOKIES:
            return redirect('home')

        form = SignUpForm()
        return render(request, 'authentication/signup.html', {'form': form})

    @staticmethod
    def post(request):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(('localhost', 50001))
            pickle.loads(sock.recv(1024))
            sock.sendall(pickle.dumps('register'))
            pickle.loads(sock.recv(1024))

            form = SignUpForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                fullname = form.cleaned_data['fullname']
                password = form.cleaned_data['password']
                sock.sendall(pickle.dumps(f'{username} {email} {fullname} {password}'))
                response = pickle.loads(sock.recv(1024))

                if response.startswith('token:'):
                    token = response.split()[1]
                    response = redirect('home')
                    response.set_cookie('token', token)
                    messages.success(request, 'You are now registered.')
                    return response
                else:
                    messages.error(request, response)
                    return redirect('signup')
