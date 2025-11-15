from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import ToDo


class TodoForm(ModelForm):

    class Meta:
        model = ToDo
        fields = ['title', 'description', 'deadline_datetime', 'important']
        widgets = {
            'deadline_datetime': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'custom-date'},
                format="%Y-%m-%dT%H:%M",
            ),
            'important': forms.CheckboxInput(attrs={'class': 'custom-checkbox'}),
            'title': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'What needs to be done?', 'maxlength':100}),
            'description': forms.Textarea(attrs={'class': 'custom-textarea', 'placeholder': 'Add more details about this task...', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label_suffix = ""
        self.fields['deadline_datetime'].input_formats = ["%Y-%m-%dT%H:%M"]


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "your@email.com"
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
            field.widget.attrs.update({"class": "form-control", })

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
        }),
        label="Username",
        label_suffix="",
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
        }),
        label="Password",
        label_suffix="",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

