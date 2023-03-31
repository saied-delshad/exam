from rest_framework import permissions

class IsSubscribedInSession(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if obj in request.user.subject_exams.all():
                return True
        return False
