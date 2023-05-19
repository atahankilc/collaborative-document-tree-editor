from django.shortcuts import render, redirect
from django.views import View
from .forms.editor import *
from .forms.document import *

import sys

sys.path.append("..")
from client.ClientHandler import ClientHandler


# ClientHandler.client_dict

class Editor(View):
    @staticmethod
    def get(request):
        if 'token' not in request.COOKIES:
            return redirect('home')

        new_document = NewDocument()
        open_document = OpenDocument()
        return render(request, 'document_editor/editor.html', {
            'new_document': new_document,
            'open_document': open_document,
        })


class Document(View):
    @staticmethod
    def get(request, document_id):
        if 'token' not in request.COOKIES:
            return redirect('home')

        server_response = f"<document>{document_id}</document>"

        select_element = SelectElementForm()
        return render(request, 'document_editor/document.html', {
            'select_element': select_element,
            'server_response': server_response
        })


class InvalidPath(View):

    @staticmethod
    def get(request, invalid_path):
        return redirect('editor')
