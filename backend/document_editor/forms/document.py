from django import forms


class SetDocumentName(forms.Form):
    set_document_name = forms.CharField()
    set_document_name.label = "Document Name"


class SelectElement(forms.Form):
    select_element = forms.CharField()
    select_element.label = "Element Id"


class InsertElement(forms.Form):
    element_type = forms.CharField()
    element_type.label = "Element Type"
    element_position = forms.IntegerField()
    element_position.label = "Element Position"
    element_id = forms.IntegerField()
    element_id.label = "Element Id"


class UpdateElement(forms.Form):
    element_type = forms.CharField()
    element_type.label = "Element Type"
    element_position = forms.IntegerField()
    element_position.label = "Element Position"
    element_id = forms.IntegerField()
    element_id.label = "Element Id"


class SetElementAttribute(forms.Form):
    attr_name = forms.CharField()
    attr_name.label = "Attribute Name"
    attr_value = forms.IntegerField()
    attr_value.label = "Attribute Value"


class DeleteElement(forms.Form):
    element_position = forms.IntegerField()
    element_position.label = "Element Position"


class ExportDocument(forms.Form):
    export_format = forms.ChoiceField(choices=[('html', 'HTML')])
    export_format.label = "Export Format"
    export_path = forms.CharField()
    export_path.label = "Export Path"
    doc_name = forms.CharField()
    doc_name.label = "Document Name"
