from rest_framework import permissions

class IsSubscribedInSession(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method in ['GET']:
            return True
        return False


    def has_object_permission(self, request, view, obj):
        
        if request.method in ['GET']:
            return True
        return False


class ExamResultOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.student:
            if obj.is_finished and request.method == "GET":
                return True
            elif obj.is_finished:
                return False
            return True
        return False
    

class IsNetRise(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.username == 'netrise':
            return True
        return False
    