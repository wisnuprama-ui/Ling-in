from django import forms
from .models import Status, Comment

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
        'max-length':350,
        'cols': 100,
        'rows': 4,
        'onkeydown': 'calculateChar()',
        'onpaste': 'calculateChar()',
    }

    content = forms.CharField(label='',
                              max_length=350,
                              required=True,
                              widget=forms.Textarea(attrs=status_attrs))

    class Meta:
        model = Status


class CommentForm(forms.Form):
    """
    Description:
    Form for input comment to the status from user
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

    # username = forms.CharField(label='',
    #                           max_length=128,
    #                           required=True,
    #                           widget=forms.Textarea(attrs=status_attrs))

    content = forms.CharField(label='',
                              max_length=350,
                              required=True,
                              widget=forms.Textarea(attrs=status_attrs))

    class Meta:
        model = Comment
