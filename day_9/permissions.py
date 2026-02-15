from rest_framework.permissions import BasePermission


class MyCustomPermissionClass(BasePermission):

    def has_permission(self, request, view):
        return request.user

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author