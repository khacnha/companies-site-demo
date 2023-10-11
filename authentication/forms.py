from django import forms
from django.contrib.auth.forms import UserCreationForm
from authentication.models import User


class SignupForm(UserCreationForm):
    """
    Sign up form
    """

    email = forms.EmailField(max_length=200, help_text="Required")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password1"],
        )
        return user
