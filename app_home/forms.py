from django import forms
from app_profile.models import UserProfile

# Form

class LoginForm(forms.Form):
    """
    Description:
    Form to input username

    """
    error_message = {
        'required':'This field is required'
    }

    status_attrs = {
        'type':'text',
        'class':'login-form-input',
        'placeholder':'What is your username?',
        'cols': 100,
        'rows': 1,
    }

    username = forms.CharField(label='',
                              required=True,
                              widget=forms.TextInput(attrs=status_attrs))

class SignUpForm(forms.Form):
    """
    Description:
    Form to create username
    """
    error_message = {
        'required':'This field is required'
    }

    input_attrs = {
        'type':'text',
        'class':'signup-form-input',
        'placeholder':'',
        'cols': 100,
        'rows': 1,
    }

    username = forms.CharField(label='Username*',
                               required=True,
                               widget=forms.TextInput(attrs=input_attrs))

    first_name = forms.CharField(label='First Name*',
                                 required=True,
                                 widget=forms.TextInput(attrs=input_attrs))

    middle_name = forms.CharField(label='Middle Name',
                                  required=False,
                                  widget=forms.TextInput(attrs=input_attrs))

    last_name = forms.CharField(label='Last Name*',
                                required=True,
                                widget=forms.TextInput(attrs=input_attrs))

    email = forms.EmailField(label='Email*',
                            required=True,
                            widget=forms.EmailInput(attrs=input_attrs))

    gender = forms.ChoiceField(label='Gender',
                             required=True,
                             choices=UserProfile.GENDER_CHOICE)


    class Meta:
        model = UserProfile