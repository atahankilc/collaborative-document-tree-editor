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
                response = client.pop_from_receiving_queue()
                if response == 'Document opened successfully':
                    messages.success(request, response)
                    response = redirect('document', document_id=document_id)
                    response.set_cookie('documentid', document_id)
                    return response
                else:
                    messages.error(request, response)
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

        client = ClientHandler.get_session(request.session.session_key)
        client.add_to_sending_queue(f'get_element_xml')
        server_message = ''
        server_response = ''
        while (True):
            message = client.pop_from_receiving_queue()
            if message.startswith('<'):
                server_response = message
                break
            server_message += message + '\n'

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
            'server_message': server_message,
            'server_response': server_response
        })

    @staticmethod
    def post(request, document_id):
        client = ClientHandler.get_session(request.session.session_key)

        if 'set_document_name' in request.POST:
            set_document_name = SetDocumentName(request.POST)
            if set_document_name.is_valid():
                document_name = set_document_name.cleaned_data['set_document_name']
                client.add_to_sending_queue(f"set_document_name {document_name}")
                response = redirect('document', document_id=document_id)
                return response
        elif 'select_element' in request.POST:
            selected_element = SelectElement(request.POST)
            if selected_element.is_valid():
                selected_element = selected_element.cleaned_data['select_element']
                client.add_to_sending_queue(f"select_element {selected_element}")
                response = redirect('document', document_id=document_id)
                return response
        elif 'insert_element' in request.POST:
            inserted_element = InsertElement(request.POST)
            if inserted_element.is_valid():
                element_type = inserted_element.cleaned_data['element_type']
                element_position = inserted_element.cleaned_data['element_position']
                element_id = inserted_element.cleaned_data['element_id']
                client.add_to_sending_queue(f"insert_element {element_type} {element_position} {element_id}")
                response = redirect('document', document_id=document_id)
                return response
        elif 'update_element' in request.POST:
            update_element = UpdateElement(request.POST)
            if update_element.is_valid():
                element_type = update_element.cleaned_data['element_type']
                element_position = update_element.cleaned_data['element_position']
                element_id = update_element.cleaned_data['element_id']
                client.add_to_sending_queue(f"update_element {element_type} {element_position} {element_id}")
                response = redirect('document', document_id=document_id)
                return response
        elif 'set_element_attribute' in request.POST:
            element_attribute = SetElementAttribute(request.POST)
            if element_attribute.is_valid():
                attr_name = element_attribute.cleaned_data['attr_name']
                attr_value = element_attribute.cleaned_data['attr_value']
                client.add_to_sending_queue(f"set_element_attribute {attr_name} {attr_value}")
                response = redirect('document', document_id=document_id)
                return response
        elif 'delete_element' in request.POST:
            deleted_element = DeleteElement(request.POST)
            if deleted_element.is_valid():
                element_position = deleted_element.cleaned_data['element_position']
                client.add_to_sending_queue(f"delete_element {element_position}")
                response = redirect('document', document_id=document_id)
                return response
        elif 'export_document' in request.POST:
            export_document = ExportDocument(request.POST)
            if export_document.is_valid():
                export_format = export_document.cleaned_data['export_format']
                export_path = export_document.cleaned_data['export_path']
                doc_name = export_document.cleaned_data['doc_name']
                client.add_to_sending_queue(f"export {export_format} {export_path} {doc_name}")
                response = redirect('document', document_id=document_id)
                return response
        elif 'close_document' in request.POST:
            client.add_to_sending_queue(f"close_document")
            while (True):
                message = client.pop_from_receiving_queue()
                if message == 'Document closed successfully':
                    break
            messages.success(request, message)
            response = redirect('editor')
            response.delete_cookie("documentid")
            return response
        else:
            print("no match", request.POST)
            return redirect('document', document_id)
