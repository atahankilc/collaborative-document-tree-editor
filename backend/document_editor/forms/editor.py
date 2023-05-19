from django import forms


class NewDocument(forms.Form):
    new_document = forms.CharField()
    new_document.label = "Document Template File"


class OpenDocument(forms.Form):
    document_id = forms.CharField()
    document_id.label = "Document Id"
