from django_registration.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField

from users.models import CustomUser

class CustomUserForm(RegistrationForm):

    class Meta(RegistrationForm.Meta):
        model = CustomUser


class CustomLoginForm(AuthenticationForm):

    captcha = CaptchaField(label = "Enter the result")