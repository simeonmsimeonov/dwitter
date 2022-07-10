from django import forms
from web.models import Dweet, Tag, User


class RegistrationForm(forms.ModelForm):
    email = forms.CharField(
        required=True
    )

    password = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={
                "type": "password"
            }
        )
    )

    first_name = forms.CharField(
        required=True
    )

    last_name = forms.CharField(
        required=True
    )

 
    class Meta:
        model = User
        fields = ["email", "username", "password", "first_name", "last_name"]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "password"]

class DweetForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Write a state...",
                "class": "textinput is-info is-normal"
            }
        ),
        label="",
        )
    
    tag = forms.ModelChoiceField(
        queryset=Tag.objects.all(), 
        label="How are you feeling?", 
        widget=forms.widgets.Select(attrs={
        
            "class": "select is-info is-rounded"
    }), required=False)

    class Meta:
        model = Dweet
        exclude = ("user",)


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name", "username", "profile_image", "bio", )