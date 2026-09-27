from rest_framework.permissions import BasePermission


class IsAgentOrAdmin(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role in ["AGENT", "ADMIN"]
        )

class IsPropertyOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):

        return (
            request.user.role == "ADMIN"
            or obj.owner == request.user
        )