from django.views import View
from django.shortcuts import render, redirect

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
            response = render(request, 'home/base.html', {})
            response.delete_cookie('token')
            response.delete_cookie('documentid')
        elif 'documentid' in request.COOKIES:
            response = redirect('document', document_id=request.COOKIES['documentid'])
        elif 'token' in request.COOKIES:
            response = render(request, 'home/base.html', {'token': request.COOKIES['token']})
        else:
            response = render(request, 'home/base.html')
        return response
