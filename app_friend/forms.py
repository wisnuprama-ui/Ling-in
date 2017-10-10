from django import forms

class Message_Form(forms.Form):
    error_messages = {
        'required': 'Tolong isi input ini',
        'invalid': 'Isi input dengan app Heroku Anda',
    }
    attrs = {
        'class': 'form-control'
    }

    name = forms.CharField(label='Nama', required=True, max_length=27, widget=forms.TextInput(attrs=attrs))
    url = forms.URLField(required=True, widget=forms.URLInput(attrs=attrs))
    
