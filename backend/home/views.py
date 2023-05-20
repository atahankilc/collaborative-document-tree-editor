from django.views import View
from django.shortcuts import render, redirect

import sys

sys.path.append("..")
from client.ClientHandler import ClientHandler


class Home(View):
    @staticmethod
    def get(request):
        session_key = request.session.session_key
        if session_key not in ClientHandler.client_dict:
            ClientHandler.add_session(session_key)
        context = {}
        if 'token' in request.COOKIES:
            context['token'] = request.COOKIES['token']
        return render(request, 'home/base.html', context)
