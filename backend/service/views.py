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


class DocumentXML(View):
    @staticmethod
    def get(request):
        if 'documentid' in request.COOKIES:
            ClientHandler.send_to_session(request.COOKIES['sessionid'], 'get_element_xml', request.COOKIES['token'])
            server_response = ClientHandler.receive_from_session(request.COOKIES['sessionid'], '<')
            return JsonResponse({'server_response': server_response})
