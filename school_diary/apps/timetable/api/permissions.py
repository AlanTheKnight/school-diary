from rest_framework import permissions


class StudentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_student()


class StudentInKlassPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_student() and request.user.student.in_klass()
