from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from users.api.serializers import UserDisplaySerializer
from users.models import CustomUser


class UserDisplayAPIViewset(viewsets.ModelViewSet):

    queryset = CustomUser.objects.all()
    lookup_field = "id"
    serializer_class = UserDisplaySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        if self.request.user.is_authenticated:
            session_queryset = CustomUser.objects.get(user=self.request.user)
        return session_queryse
