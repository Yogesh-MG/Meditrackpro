from rest_framework import serializers
from .models import Ticket, TicketComment
from django.contrib.auth.models import User
from device.serializers import DeviceSerializer
from device.models import Device
from employees.models import Employee
from hospitals.serilaizers import HospitalSerializer  # Fixed typo: serilaizers -> serializers
from employees.serializers import EmployeeSerializer
from django.utils import timezone

class TicketCommentSerializer(serializers.ModelSerializer):
    author = EmployeeSerializer(read_only=True)
    author_id = serializers.CharField(write_only=True, required=True)
    file = serializers.FileField(allow_null=True, required=False)

    class Meta:
        model = TicketComment
        fields = ['id', 'ticket', 'author', 'author_id', 'content', 'file', 'created_at']
        read_only_fields = ['ticket', 'created_at']

    def validate_author_id(self, value):
        print(f"Validating author_id: {value}")  # Debug log
        try:
            employee = Employee.objects.get(employee_id=value)
            print(f"Found employee: {employee}")  # Debug log
            return employee.id
        except Employee.DoesNotExist:
            print(f"Employee with ID {value} does not exist")  # Debug log
            raise serializers.ValidationError(f"Employee with ID {value} does not exist.")

    def validate(self, data):
        if not data.get('content').strip():
            raise serializers.ValidationError({"content": "Comment can’t be empty!"})
        if data.get('file'):
            max_size = 5 * 1024 * 1024  # 5MB
            if data['file'].size > max_size:
                raise serializers.ValidationError({"file": "File’s too big! Keep it under 5MB."})
        return data

class TicketSerializer(serializers.ModelSerializer):
    device = DeviceSerializer(read_only=True)
    device_id = serializers.PrimaryKeyRelatedField(
        queryset=Device.objects.all(), source='device', write_only=True, allow_null=True
    )
    created_by = EmployeeSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, allow_null=False)  # Require created_by_id
    assigned_to = EmployeeSerializer(read_only=True, allow_null=True)
    assigned_to_id = serializers.CharField(write_only=True, allow_null=True)
    hospital = HospitalSerializer(read_only=True)
    comments = TicketCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'ticket_id', 'hospital', 'title', 'device', 'device_id', 'category',
            'priority', 'status', 'location', 'created_by', 'created_by_id', 'assigned_to',
            'assigned_to_id', 'description', 'created_at', 'updated_at', 'comments'
        ]
        read_only_fields = ['ticket_id', 'hospital', 'created_at', 'updated_at']

    def validate_created_by_id(self, value):
        try:
            employee = Employee.objects.get(employee_id=value)
            print(f"Validated created_by_id: {value} -> {employee}")  # Debug log
            return employee
        except Employee.DoesNotExist:
            raise serializers.ValidationError(f"Employee with ID {value} does not exist.")

    def validate_assigned_to_id(self, value):
        if not value:
            return None
        try:
            employee = Employee.objects.get(employee_id=value)  # Use employee_id, not id
            if employee.role != 'engineer':  # Ensure role is 'engineer'
                raise serializers.ValidationError(f"Employee with ID {value} must be a Biomedical Engineer.")
            print(f"Validated assigned_to_id: {value} -> {employee}")  # Debug log
            return employee.id
        except Employee.DoesNotExist:
            raise serializers.ValidationError(f"Employee with ID {value} does not exist.")

    def validate(self, data):
        # Skip validation for partial updates (PATCH)
        if self.partial:
            return data
        # Full validation for POST
        if not data.get('title'):
            raise serializers.ValidationError({"title": "Title cannot be empty, bro!"})
        if len(data.get('title')) < 3:
            raise serializers.ValidationError({"title": "Title needs at least 3 characters."})
        if not data.get('description'):
            raise serializers.ValidationError({"description": "Gotta describe the issue!"})
        if len(data.get('description')) < 10:
            raise serializers.ValidationError({"description": "Description needs at least 10 characters."})
        if not data.get('location'):
            raise serializers.ValidationError({"location": "Where’s this happening? Add a location."})
        if not data.get('category'):
            raise serializers.ValidationError({"category": "Specify a category."})
        return data

    def create(self, validated_data):
        print("Validated Data:", validated_data)  # Debug log
        # Extract created_by_id and map to created_by
        created_by_employee = validated_data.pop('created_by_id', None)
        if not created_by_employee:
            raise serializers.ValidationError({"created_by_id": "Employee is required."})
        validated_data['created_by'] = created_by_employee
        # Extract assigned_to_id and map to assigned_to
        assigned_to_employee = validated_data.pop('assigned_to_id', None)
        if assigned_to_employee:
            validated_data['assigned_to'] = assigned_to_employee
        # Remove device_id if present (handled by source='device')
        validated_data.pop('device_id', None)
        print("Data before save:", validated_data)  # Debug log
        ticket = Ticket.objects.create(**validated_data)
        print("Created ticket:", ticket)  # Debug log
        return ticket