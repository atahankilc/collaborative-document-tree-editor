from django import forms


class SelectElement(forms.Form):
    select_element = forms.CharField()
    select_element.label = "Select Element With Id"
