from django import forms
from .models import CustomUser, AddCash, Expense

from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
)



# Registration Form

class RegistrationForm(UserCreationForm):

    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Choose a Username",
            "autocomplete": "username",
        })
    )

    display_name = forms.CharField(
        label="Display Name",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Display Name",
        })
    )

    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Email Account",
            "autocomplete": "email",
        })
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Password",
            "autocomplete": "new-password",
        })
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirm Password",
            "autocomplete": "new-password",
        })
    )

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "display_name",
            "email",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "This email is already registered."
            )

        return email


# Login Form
class LoginForm(AuthenticationForm):

    username = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Username or Email",
            "autocomplete": "username",
        })
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Password",
            "autocomplete": "current-password",
        })
    )



# Change Password Form

class ChangePasswordForm(PasswordChangeForm):

    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Old Password",
            "autocomplete": "current-password",
        })
    )

    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "New Password",
            "autocomplete": "new-password",
        })
    )

    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirm New Password",
            "autocomplete": "new-password",
        })
    )



# Add Cash / Income Form

class AddCashForm(forms.ModelForm):

    class Meta:
        model = AddCash

        fields = [
            "source",
            "datetime",
            "amount",
            "description",
        ]

        widgets = {
            "source": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter income source",
            }),

            "datetime": forms.DateTimeInput(attrs={
                "class": "form-control",
                "type": "datetime-local",
            }),

            "amount": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter amount",
                "step": "0.01",
                "min": "0.01",
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter description",
                "rows": 3,
            }),
        }



# Expense Form

class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense

        fields = [
            "amount",
            "datetime",
            "description",
        ]

        widgets = {
            "amount": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter expense amount",
                "step": "0.01",
                "min": "0.01",
            }),

            "datetime": forms.DateTimeInput(attrs={
                "class": "form-control",
                "type": "datetime-local",
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter expense description",
                "rows": 3,
            }),
        }