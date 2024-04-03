from django.contrib import admin
from OnlineExam.forms import CustomAdminLogin


class ExamAdminSite(admin.AdminSite):
    login_form=CustomAdminLogin