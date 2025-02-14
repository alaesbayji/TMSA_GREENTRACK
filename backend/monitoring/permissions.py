from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Admin').exists()

class IsResponsableEntreprise(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='ResponsableEntreprise').exists()

class IsResponsableSuivi(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='ResponsableSuiviTMSA').exists()
