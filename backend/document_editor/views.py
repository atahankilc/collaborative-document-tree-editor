from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from .forms.editor import *
from .forms.document import *

import sys

sys.path.append("..")
from client.ClientHandler import ClientHandler


class Editor(View):
    @staticmethod
    def get(request):
        if ('token' not in request.COOKIES) or (not request.session.exists(request.session.session_key)):
            return redirect('home')

        client = ClientHandler.get_session(request.session.session_key)
        client.add_to_sending_queue(f'list_documents')
        server_response = client.pop_from_receiving_queue()

        new_document = NewDocument()
        open_document = OpenDocument()
        return render(request, 'document_editor/editor.html', {
            'new_document': new_document,
            'open_document': open_document,
            'server_response': server_response
        })

    @staticmethod
    def post(request):
        client = ClientHandler.get_session(request.session.session_key)

        if 'new_document' in request.POST:
            new_document = NewDocument(request.POST)
            if new_document.is_valid():
                document_template = new_document.cleaned_data['new_document']
                client.add_to_sending_queue(f"new_document {document_template}")
                messages.success(request, client.pop_from_receiving_queue())
                return redirect('editor')
        elif 'open_document' in request.POST:
            open_document = OpenDocument(request.POST)
            if open_document.is_valid():
                document_id = open_document.cleaned_data['open_document']
                client.add_to_sending_queue(f"open_document {document_id}")
                messages.success(request, client.pop_from_receiving_queue())
                response = redirect('document', document_id=document_id)
                response.set_cookie('documentid', document_id)
                return response
        else:
            return redirect('editor')


class Document(View):
    @staticmethod
    def get(request, document_id):
        if ('token' not in request.COOKIES) or (not request.session.exists(request.session.session_key)):
            return redirect('home')

        client = ClientHandler.get_session(request.session.session_key)
        client.add_to_sending_queue(f'get_element_xml')
        server_response = client.pop_from_receiving_queue()

        select_element = SelectElement()
        return render(request, 'document_editor/document.html', {
            'select_element': select_element,
            'server_response': server_response
        })

    @staticmethod
    def post(request, document_id):
        client = ClientHandler.get_session(request.session.session_key)

        if 'select_element' in request.POST:
            selected_element = SelectElement(request.POST)
            if selected_element.is_valid():
                selected_element = selected_element.cleaned_data['select_element']
                client.add_to_sending_queue(f"select_element {selected_element}")
                messages.success(request, client.pop_from_receiving_queue())
                response = redirect('document', document_id=document_id)
                return response
        elif 'close_document' in request.POST:
            client.add_to_sending_queue(f"close_document")
            messages.success(request, client.pop_from_receiving_queue())
            response = redirect('editor')
            response.delete_cookie("documentid")
            return response
        else:
            return redirect('document', document_id)
