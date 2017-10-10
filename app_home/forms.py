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
        'cols': 50,
        'rows': 1,
    }

    date_attrs = {
        'type':'datetime-local',
        'name':'date',
        'id':'date',
        'class':'signup-form-input',
    }

    photo_attrs = {
        'class':'signup-form-input',
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

    birth_date = forms.DateField(label='Birth Date*',
                                required=True,
                                widget=forms.SelectDateWidget(
                                    date_attrs
                                ))

    gender = forms.ChoiceField(label='Gender*',
                             required=True,
                             choices=UserProfile.GENDER_CHOICE,
                             widget=forms.Select(input_attrs))

    photo = forms.ImageField(label='Photo',
                            required=False,
                            widget=forms.ClearableFileInput(photo_attrs))

    class Meta:
        model = UserProfile