from django import forms


class SelectElementForm(forms.Form):
    selected_element = forms.CharField()
    selected_element.label = "Select Element With Id"
