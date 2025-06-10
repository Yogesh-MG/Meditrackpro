from rest_framework import permissions
from employees.models import Employee

class IsTechnicianOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # Admins can do anything
        if request.user.is_staff or request.user.is_superuser:
            return True
        # Check if user is a Engineer
        try:
            employee = request.user.employee_profile  # OneToOne link
            return employee.role == 'engineer'
        except Employee.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        # Ensure the technician belongs to the same hospital as the device
        if request.user.is_staff or request.user.is_superuser:
            return True
        employee = request.user.employee_profile
        return employee.role == 'engineer' and obj.hospital == employee.hospital
    

class IsTechnician(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            employee = request.user.employee_profile  # OneToOne link
            return employee.role == 'engineer'
        except Employee.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        # Ensure the technician belongs to the same hospital as the device
        if request.user.is_staff or request.user.is_superuser:
            return True
        employee = request.user.employee_profile
        return employee.role == 'engineer' and obj.hospital == employee.hospital
    

class IsInventoryManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # Admins can do anything
        if request.user.is_staff or request.user.is_superuser:
            return True
        try:
            employee = request.user.employee_profile  # OneToOne link
            return employee.role == 'engineer'
        except Employee.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        # Ensure the technician belongs to the same hospital as the device
        if request.user.is_staff or request.user.is_superuser:
            return True
        employee = request.user.employee_profile
        return employee.role == 'technician' and obj.hospital == employee.hospital