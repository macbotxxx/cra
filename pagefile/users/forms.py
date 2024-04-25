from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import User


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User
        field_classes = {"email": EmailField}


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """


class LoginForm(forms.Form):
    userID = forms.CharField(
        required=True
    )
    password = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'type': 'password'})
    )

    def __init__(self, *args, **kwargs):
        # user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # if user and user.is_authenticated:
        #     self.fields['first_name'].initial = user.first_name

        # Loop through each field in the form and set the widget's class attribute
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
