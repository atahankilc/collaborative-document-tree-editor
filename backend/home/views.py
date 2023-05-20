from django.views import View
from django.shortcuts import render

import sys

sys.path.append("..")
from client.ClientHandler import ClientHandler


class Home(View):
    @staticmethod
    def get(request):
        if not request.session.exists(request.session.session_key):
            request.session.create()
        session_key = request.session.session_key
        if session_key not in ClientHandler.client_dict:
            ClientHandler.add_session(session_key)
        print(ClientHandler.client_dict)
        context = {}
        if 'token' in request.COOKIES:
            context['token'] = request.COOKIES['token']
        return render(request, 'home/base.html', context)
