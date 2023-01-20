from rest_framework import permissions

class ServicePermissionAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='api_gateway').exists()
