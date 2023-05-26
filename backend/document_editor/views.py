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
        if ('token' not in request.COOKIES) or \
                ('documentid' in request.COOKIES) or \
                (request.session.session_key not in ClientHandler.client_dict):
            return redirect('home')

        command = 'list_documents'
        ClientHandler.send_to_session(request.session.session_key, command, request.COOKIES["token"])
        server_response = ClientHandler.receive_from_session(request.session.session_key, '')

        new_document = NewDocument()
        open_document = OpenDocument()
        return render(request, 'document_editor/editor.html', {
            'new_document': new_document,
            'open_document': open_document,
            'server_response': server_response
        })

    @staticmethod
    def post(request):
        if 'new_document' in request.POST:
            new_document = NewDocument(request.POST)
            if new_document.is_valid():
                document_template = new_document.cleaned_data['new_document']
                command = f'new_document {document_template}'
                ClientHandler.send_to_session(request.session.session_key, command, request.COOKIES["token"])
                response = ClientHandler.receive_from_session(request.session.session_key, '')
                messages.success(request, response)
                if response == "Invalid Token":
                    response = redirect('home')
                    response.delete_cookie("token")
                    return response
                return redirect('editor')
        elif 'open_document' in request.POST:
            open_document = OpenDocument(request.POST)
            if open_document.is_valid():
                document_id = open_document.cleaned_data['open_document']
                command = f' open_document {document_id}'
                ClientHandler.send_to_session(request.session.session_key, command, request.COOKIES["token"])
                response = ClientHandler.receive_from_session(request.session.session_key, '')
                messages.success(request, response)
                if response == "Invalid Token":
                    response = redirect('home')
                    response.delete_cookie("token")
                    return response
                if response == 'Document opened successfully':
                    response = redirect('document', document_id=document_id)
                    response.set_cookie('documentid', document_id)
                    return response
                else:
                    return redirect('editor')
        else:
            return redirect('editor')


class Document(View):
    @staticmethod
    def get(request, document_id):
        if ('token' not in request.COOKIES) or \
                ('documentid' not in request.COOKIES) or \
                (request.session.session_key not in ClientHandler.client_dict):
            return redirect('home')

        command = 'get_element_xml'
        ClientHandler.send_to_session(request.session.session_key, command, request.COOKIES["token"])
        server_response = ClientHandler.receive_from_session(request.session.session_key, '<')

        if server_response == "Invalid Token":
            messages.success(request, server_response)
            response = redirect('home')
            response.delete_cookie("token")
            response.delete_cookie("documentid")
            return response

        set_document_name = SetDocumentName()
        select_element = SelectElement()
        insert_element = InsertElement()
        update_element = UpdateElement()
        set_element_attribute = SetElementAttribute()
        delete_element = DeleteElement()
        export_document = ExportDocument()
        return render(request, 'document_editor/document.html', {
            'set_document_name': set_document_name,
            'select_element': select_element,
            'insert_element': insert_element,
            'update_element': update_element,
            'set_element_attribute': set_element_attribute,
            'delete_element': delete_element,
            'export_document': export_document,
            'server_response': server_response
        })

    @staticmethod
    def post(request, document_id):
        if 'set_document_name' in request.POST:
            set_document_name = SetDocumentName(request.POST)
            if set_document_name.is_valid():
                document_name = set_document_name.cleaned_data['set_document_name']
                command = f'set_document_name {document_name}'
                ClientHandler.send_to_session(request.session.session_key, command, request.COOKIES["token"])
                response = redirect('document', document_id=document_id)
                return response
        elif 'select_element' in request.POST:
            selected_element = SelectElement(request.POST)
            if selected_element.is_valid():
                selected_element = selected_element.cleaned_data['select_element']
                command = f'select_element {selected_element}'
                ClientHandler.send_to_session(request.session.session_key, command, request.COOKIES["token"])
                response = redirect('document', document_id=document_id)
                return response
        elif 'insert_element' in request.POST:
            inserted_element = InsertElement(request.POST)
            if inserted_element.is_valid():
                element_type = inserted_element.cleaned_data['element_type']
                element_position = inserted_element.cleaned_data['element_position']
                element_id = inserted_element.cleaned_data['element_id']
                command = f'insert_element {element_type} {element_position} {element_id}'
                ClientHandler.send_to_session(request.session.session_key, command, request.COOKIES["token"])
                response = redirect('document', document_id=document_id)
                return response
        elif 'update_element' in request.POST:
            update_element = UpdateElement(request.POST)
            if update_element.is_valid():
                element_type = update_element.cleaned_data['element_type']
                element_position = update_element.cleaned_data['element_position']
                element_id = update_element.cleaned_data['element_id']
                command = f'update_element {element_type} {element_position} {element_id}'
                ClientHandler.send_to_session(request.session.session_key, command, request.COOKIES["token"])
                response = redirect('document', document_id=document_id)
                return response
        elif 'set_element_attribute' in request.POST:
            element_attribute = SetElementAttribute(request.POST)
            if element_attribute.is_valid():
                attr_name = element_attribute.cleaned_data['attr_name']
                attr_value = element_attribute.cleaned_data['attr_value']
                command = f'set_element_attribute {attr_name} {attr_value}'
                ClientHandler.send_to_session(request.session.session_key, command, request.COOKIES["token"])
                response = redirect('document', document_id=document_id)
                return response
        elif 'delete_element' in request.POST:
            deleted_element = DeleteElement(request.POST)
            if deleted_element.is_valid():
                element_position = deleted_element.cleaned_data['element_position']
                command = f'delete_element {element_position}'
                ClientHandler.send_to_session(request.session.session_key, command, request.COOKIES["token"])
                response = redirect('document', document_id=document_id)
                return response
        elif 'export_document' in request.POST:
            export_document = ExportDocument(request.POST)
            if export_document.is_valid():
                export_format = export_document.cleaned_data['export_format']
                export_path = export_document.cleaned_data['export_path']
                doc_name = export_document.cleaned_data['doc_name']
                command = f'export {export_format} {export_path} {doc_name}'
                ClientHandler.send_to_session(request.session.session_key, command, request.COOKIES["token"])
                response = redirect('document', document_id=document_id)
                return response
        elif 'close_document' in request.POST:
            command = 'close_document'
            ClientHandler.send_to_session(request.session.session_key, command, request.COOKIES["token"])
            while (True):
                message = ClientHandler.receive_from_session(request.session.session_key, '')
                if message == 'Document closed successfully':
                    break
            messages.success(request, message)
            response = redirect('editor')
            response.delete_cookie("documentid")
            return response
        else:
            print("no match", request.POST)
            return redirect('document', document_id)
