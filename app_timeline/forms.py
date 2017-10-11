from django import forms
from .models import Status

# Form

class StatusPostForm(forms.Form):
    """
    Description:
    Form to input status from user

    """
    error_message = {
        'required':'This field is required'
    }

    status_attrs = {
        'type':'text',
        'class':'status-form-textarea',
        'placeholder':'What do you think?',
        'id':'status-form-textarea',
        'max-length':200,
        'cols': 100,
        'rows': 4,
        'onkeydown': 'calculateChar()',
        'onpaste': 'calculateChar()',
    }

    content = forms.CharField(label='',
                              max_length=200,
                              required=True,
                              widget=forms.Textarea(attrs=status_attrs))

    class Meta:
        model = Status