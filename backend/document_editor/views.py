from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from django.urls import reverse
from .forms.home import *
from .forms.document import *

import sys

sys.path.append("..")
from client.ClientHandler import ClientHandler


# ClientHandler.client_dict

class Home(View):
    @staticmethod
    def get(request):
        new_document = NewDocument()
        open_document = OpenDocument()
        return render(request, 'document_editor/home.html', {
            'new_document': new_document,
            'open_document': open_document,
        })


class Document(View):
    @staticmethod
    def get(request, document_id):
        server_response = f"<document>{document_id}</document>"

        select_element = SelectElementForm()
        return render(request, 'document_editor/document.html', {
            'select_element': select_element,
            'server_response': server_response
        })


class InvalidPath(View):

    @staticmethod
    def get(request, invalid_path):
        redirect_path = reverse("home")
        return HttpResponseRedirect(redirect_path)
