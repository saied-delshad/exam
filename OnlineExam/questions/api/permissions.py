from rest_framework import permissions

class IsSubscribedInSession(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if request.user.groups.filter(name = obj.participants.name).exists():
                return True
        return False
