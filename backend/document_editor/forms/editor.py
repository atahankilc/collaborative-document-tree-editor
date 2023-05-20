from django import forms


class NewDocument(forms.Form):
    new_document = forms.CharField()
    new_document.label = "Document Template File"


class OpenDocument(forms.Form):
    open_document = forms.CharField()
    open_document.label = "Document Id"
