from django import forms
from django.contrib.auth import get_user_model
from apps.organizations.models import Organization

User = get_user_model()


class CreateUserForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    role = forms.ChoiceField(
        choices=[
            ("ADMIN", "Admin"),
            ("MANAGER", "Manager"),
            ("VIEWER", "Viewer"),
        ]
    )

    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        required=True
    )

    class Meta:
        model = User
        fields = ["email", "password", "role", "organization"]