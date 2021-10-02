from django.urls import path
from users.api.views import UserDisplayAPIView


urlpatterns = [
    path('user/', UserDisplayAPIView.as_view(), name='current-user')
]