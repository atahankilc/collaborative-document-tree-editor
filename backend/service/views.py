from django.views import View
from django.http import JsonResponse

import sys

sys.path.append("..")
from client.ClientHandler import ClientHandler


class WsPort(View):
    @staticmethod
    def get(request):
        if 'sessionid' in request.COOKIES and 'token' in request.COOKIES:
            ClientHandler.send_to_session(request.COOKIES['sessionid'], '%WS_PORT%', request.COOKIES['token'])
            ws_port = ClientHandler.receive_from_session(request.COOKIES['sessionid'], '')
            return JsonResponse({'ws_port': ws_port})
