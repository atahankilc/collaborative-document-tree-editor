from django import forms


class SetDocumentName(forms.Form):
    set_document_name = forms.CharField()
    set_document_name.label = "Change Document Name"


class SelectElement(forms.Form):
    select_element = forms.CharField()
    select_element.label = "Select Element With Id"


class InsertElement(forms.Form):
    element_type = forms.CharField()
    element_type.label = "Element Type"
    position = forms.IntegerField()
    position.label = "Element Position"
    element_id = forms.IntegerField()
    element_id.label = "Element Id"
