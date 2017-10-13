from django import forms

class FriendForm(forms.Form):
    error_message = {
        'required':'This field is required'
    }

    input_attrs = {
        'type':'text',
        'class':'input-form-name',
        'id':'input-form-name',
        'placeholder':'Who is your friend?',
        'cols': 50,
        'rows': 1,
    }

    url_attrs = {
        'type':'text',
        'class':'input-form-name',
        'id':'input-form-url',
        'placeholder':'What is your friend\'s url',
        'cols': 50,
        'rows': 1,
    }


    name = forms.CharField(label='Nama', required=True,
                           widget=forms.TextInput(attrs=input_attrs),
                           error_messages=error_message)

    url = forms.URLField(label='URL',required=True,
                         widget=forms.URLInput(attrs=url_attrs),
                         error_messages=error_message)
    
