from django import forms

class FriendForm(forms.Form):
    error_message = {
        'required':'This field is required'
    }

    input_attrs = {
        'type':'text',
        'class':'input-form-textinput',
        'placeholder':'Who is your friend?',
        'cols': 100,
        'rows': 1,
    }

    input_attrs = {
        'type':'text',
        'class':'input-form-textinput',
        'placeholder':'What is your friend\'s url',
        'cols': 100,
        'rows': 1,
    }


    name = forms.CharField(label='Nama', required=True, widget=forms.TextInput(attrs=input_attrs))
    url = forms.URLField(label='URL',required=True, widget=forms.URLInput(attrs=input_attrs))
    
