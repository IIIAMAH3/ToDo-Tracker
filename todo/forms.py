from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import ToDo

class TodoForm(ModelForm):
    class Meta:
        model =  ToDo
        fields = ['title', 'description', 'important', 'deadline_datetime']
        widgets = {'deadline_datetime': forms.DateTimeInput(
            attrs={'type': 'datetime-local'},format='%Y-%m-%dT%H:%M'
        )}


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your email"
        }),
        label_suffix="",
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control",})

        self.fields["username"] = forms.CharField(
            max_length=20,
            error_messages={
                "max_length": "Username must be 30 characters or lower"
            },
            widget=forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter a username",
            })
        )

        self.fields["password1"].widget.attrs.update({
            "placeholder": "Enter password",
        })
        self.fields["password2"].widget.attrs.update({
            "placeholder": "Confirm the password",
        })

        help_texts = {
            "username": "Your username must be unique",
            "password1": "Your password must contain at least 8 characters",
        }
        for field, text in help_texts.items():
            self.fields[field].help_text = text

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter a username",
        }),
        label="Username",
        label_suffix="",
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter password",
        }),
        label="Password",
        label_suffix="",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)