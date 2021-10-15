from rest_framework import permissions

class IsSubscribedInSession(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False


class ExamResultOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.student:
            return True
        return False

    