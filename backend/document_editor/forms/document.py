from django import forms


class SetDocumentName(forms.Form):
    set_document_name = forms.CharField()
    set_document_name.label = "Change Document Name"


class SelectElement(forms.Form):
    select_element = forms.CharField()
    select_element.label = "Select Element With Id"
