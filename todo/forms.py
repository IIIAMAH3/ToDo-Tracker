from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
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
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

        self.fields["username"] = forms.CharField(
            max_length=20,
            error_messages={
                "max_length": "Username must be 30 characters or lower"
            }
        )

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control", })

        placeholders = {
            "username": "Enter a username",
            "email": "your@email.com",
            "password1": "Enter password",
            "password2": "Confirm the password",
        }

        help_texts = {
            "username": "Your username must be unique",
            "password1": "Your password must contain at least 8 characters",
            "email": "Enter a valid email address",
        }

        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs.update({
                "placeholder": placeholder
            })

        for field, text in help_texts.items():
            self.fields[field].help_text = text

    def clean_email(self):
        """
        Validate that the email is unique in the database
        This method is automatically called during form validation
        """
        email = self.cleaned_data.get("email")

        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("This email address is already in use. Please use a different email.")

        return email.lower()

    def save(self, commit=True):
        """
        Override save method to ensure email is saved
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user


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

