from django.contrib import admin
from .models import (
    School, Campus, AcademicYear, Term, Holiday, User, 
    UserSchoolMembership, Role, Permission, RolePermission, 
    UserRoleAssignment, Settings, AuditEvent, Attachment,
    Notification, NotificationDelivery, BackgroundJobRun
)


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'code', 'address', 'email')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'code', 'is_active')
    list_filter = ('school', 'is_active')
    search_fields = ('name', 'school__name', 'code')
    ordering = ('school', 'name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'start_date', 'end_date', 'is_current')
    list_filter = ('school', 'is_current', 'is_active')
    search_fields = ('name', 'school__name')
    ordering = ('-start_date',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('name', 'academic_year', 'start_date', 'end_date', 'is_active')
    list_filter = ('academic_year', 'is_active')
    search_fields = ('name', 'academic_year__name')
    ordering = ('academic_year', 'start_date')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'date', 'is_recurring')
    list_filter = ('school', 'is_recurring', 'date')
    search_fields = ('name', 'school__name')
    ordering = ('date',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'email', 'phone_number', 'is_staff', 'is_teacher', 'is_approved', 'is_active')
    list_filter = ('is_staff', 'is_teacher', 'is_approved', 'is_active', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone_number')
    list_filter = ('is_staff', 'is_teacher', 'is_approved', 'is_active', 'date_joined')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login')


@admin.register(UserSchoolMembership)
class UserSchoolMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'role', 'is_primary', 'is_active')
    list_filter = ('school', 'is_primary', 'is_active')
    search_fields = ('user__username', 'user__email', 'school__name')
    ordering = ('user', 'school')
    readonly_fields = ('joined_at',)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'codename', 'module', 'is_active')
    list_filter = ('module', 'is_active')
    search_fields = ('name', 'codename', 'module')
    ordering = ('module', 'name')
    readonly_fields = ()


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'permission', 'granted_at')
    list_filter = ('role', 'permission')
    search_fields = ('role__name', 'permission__name')
    ordering = ('role', 'permission')
    readonly_fields = ('granted_at',)


@admin.register(UserRoleAssignment)
class UserRoleAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'school', 'assigned_at', 'is_active')
    list_filter = ('role', 'school', 'is_active')
    search_fields = ('user__username', 'role__name', 'school__name')
    ordering = ('-assigned_at',)
    readonly_fields = ('assigned_at',)


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('school', 'timezone', 'default_currency', 'maintenance_mode')
    list_filter = ('maintenance_mode', 'default_currency')
    search_fields = ('school__name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = ('entity_type', 'entity_id', 'action_type', 'actor', 'timestamp')
    list_filter = ('action_type', 'entity_type', 'timestamp', 'school')
    search_fields = ('entity_type', 'entity_id', 'actor__username', 'change_reason')
    ordering = ('-timestamp',)
    readonly_fields = ('school', 'campus', 'actor', 'actor_role', 'action_type', 
                      'entity_type', 'entity_id', 'previous_data', 'new_data', 
                      'change_reason', 'ip_address', 'user_agent', 'request_id', 'timestamp')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('original_filename', 'school', 'uploaded_by', 'file_size', 'uploaded_at')
    list_filter = ('school', 'is_public', 'uploaded_at')
    search_fields = ('original_filename', 'description')
    ordering = ('-uploaded_at',)
    readonly_fields = ('uploaded_by', 'file', 'original_filename', 'file_size', 
                      'mime_type', 'uploaded_at')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'recipient', 'notification_type', 'channel', 'is_read', 'created_at')
    list_filter = ('notification_type', 'channel', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'recipient__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


@admin.register(NotificationDelivery)
class NotificationDeliveryAdmin(admin.ModelAdmin):
    list_display = ('notification', 'channel', 'status', 'attempt_count', 'created_at')
    list_filter = ('channel', 'status', 'created_at')
    search_fields = ('notification__title', 'provider_message_id', 'failure_reason')
    ordering = ('-created_at',)
    readonly_fields = ('notification', 'channel', 'provider_message_id', 'status', 
                      'attempt_count', 'last_attempt_at', 'delivered_at', 'failure_reason', 
                      'created_at', 'updated_at')


@admin.register(BackgroundJobRun)
class BackgroundJobRunAdmin(admin.ModelAdmin):
    list_display = ('job_name', 'school', 'status', 'progress_percentage', 'created_at')
    list_filter = ('status', 'school', 'created_at')
    search_fields = ('job_name', 'error_message')
    ordering = ('-created_at',)
    readonly_fields = ('job_name', 'school', 'status', 'started_at', 'completed_at', 
                      'progress_percentage', 'result_data', 'error_message', 'triggered_by', 
                      'created_at', 'updated_at')