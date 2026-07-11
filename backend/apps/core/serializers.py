from rest_framework import serializers
from .models import (
    School, Campus, AcademicYear, Term, Holiday, User, 
    UserSchoolMembership, Role, Permission, RolePermission, 
    UserRoleAssignment, Settings, AuditEvent, Attachment,
    Notification, NotificationDelivery, BackgroundJobRun
)


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'


class CampusSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)
    
    class Meta:
        model = Campus
        fields = '__all__'


class AcademicYearSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)
    
    class Meta:
        model = AcademicYear
        fields = '__all__'


class TermSerializer(serializers.ModelSerializer):
    academic_year_name = serializers.CharField(source='academic_year.name', read_only=True)
    
    class Meta:
        model = Term
        fields = '__all__'


class HolidaySerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)
    
    class Meta:
        model = Holiday
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserSchoolMembershipSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    school_name = serializers.CharField(source='school.name', read_only=True)
    
    class Meta:
        model = UserSchoolMembership
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class RolePermissionSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    permission_name = serializers.CharField(source='permission.name', read_only=True)
    permission_codename = serializers.CharField(source='permission.codename', read_only=True)
    permission_module = serializers.CharField(source='permission.module', read_only=True)
    
    class Meta:
        model = RolePermission
        fields = '__all__'


class UserRoleAssignmentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    role_name = serializers.CharField(source='role.name', read_only=True)
    school_name = serializers.CharField(source='school.name', read_only=True)
    assigned_by_name = serializers.CharField(source='assigned_by.get_full_name', read_only=True)
    
    class Meta:
        model = UserRoleAssignment
        fields = '__all__'


class SettingsSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)
    
    class Meta:
        model = Settings
        fields = '__all__'


class AuditEventSerializer(serializers.ModelSerializer):
    actor_name = serializers.CharField(source='actor.get_full_name', read_only=True)
    entity_type_display = serializers.CharField(source='get_entity_type_display', read_only=True)
    action_type_display = serializers.CharField(source='get_action_type_display', read_only=True)
    
    class Meta:
        model = AuditEvent
        fields = '__all__'
        read_only_fields = ('school', 'campus', 'actor', 'actor_role', 'action_type', 
                           'entity_type', 'entity_id', 'previous_data', 'new_data', 
                           'change_reason', 'ip_address', 'user_agent', 'request_id', 'timestamp')


class AttachmentSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    
    class Meta:
        model = Attachment
        fields = '__all__'
        read_only_fields = ('uploaded_by', 'file', 'original_filename', 'file_size', 
                           'mime_type', 'uploaded_at')


class NotificationSerializer(serializers.ModelSerializer):
    recipient_name = serializers.CharField(source='recipient.get_full_name', read_only=True)
    
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('created_at',)


class NotificationDeliverySerializer(serializers.ModelSerializer):
    notification_title = serializers.CharField(source='notification.title', read_only=True)
    
    class Meta:
        model = NotificationDelivery
        fields = '__all__'
        read_only_fields = ('notification', 'channel', 'provider_message_id', 'status', 
                           'attempt_count', 'last_attempt_at', 'delivered_at', 'failure_reason', 
                           'created_at', 'updated_at')


class BackgroundJobRunSerializer(serializers.ModelSerializer):
    job_name_display = serializers.CharField(source='get_job_name_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    triggered_by_name = serializers.CharField(source='triggered_by.get_full_name', read_only=True)
    school_name = serializers.CharField(source='school.name', read_only=True)
    
    class Meta:
        model = BackgroundJobRun
        fields = '__all__'
        read_only_fields = ('job_name', 'school', 'status', 'started_at', 'completed_at', 
                           'progress_percentage', 'result_data', 'error_message', 'triggered_by', 
                           'created_at', 'updated_at')