from django.contrib.admin.forms import AdminAuthenticationForm
from captcha.fields import CaptchaField


class CustomAdminLogin(AdminAuthenticationForm):
    captcha = CaptchaField(label = "Enter the result")
