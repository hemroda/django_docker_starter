from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget = forms.TextInput(
            attrs={"class": "form-field", "placeholder": "Username"}
        )
        self.fields["username"].label = ""

        self.fields["password"].widget = forms.PasswordInput(
            attrs={"class": "form-field mt-3", "placeholder": "Password"}
        )
        self.fields["password"].label = ""


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields
