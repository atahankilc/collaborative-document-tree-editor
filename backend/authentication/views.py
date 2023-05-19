import pickle
import socket

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import LoginForm, SignUpForm


class Login(View):
    def get(self, request):
        if 'token' in request.COOKIES:
            return redirect('home')

        form = LoginForm()
        return render(request, 'authentication/login.html', {'form': form})

    def post(self, request):
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
    def get(self, request):
        if 'token' in request.COOKIES:
            return redirect('home')

        form = SignUpForm()
        return render(request, 'authentication/signup.html', {'form': form})

    def post(self, request):
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
                    return HttpResponse(response)
