from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """Abstract base model with timestamp fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class School(models.Model):
    """
    School model representing an educational institution.
    """
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='school/logos/', blank=True, null=True)
    letterhead = models.ImageField(upload_to='school/letterheads/', blank=True, null=True)
    established_year = models.PositiveIntegerField(null=True, blank=True)
    affiliation_number = models.CharField(max_length=50, blank=True)
    board_affiliation = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'schools'
        verbose_name = _('School')
        verbose_name_plural = _('Schools')
        ordering = ['name']

    def __str__(self):
        return self.name


class Campus(models.Model):
    """
    Campus model for multi-campus schools.
    """
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='campuses')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'campuses'
        verbose_name = _('Campus')
        verbose_name_plural = _('Campuses')
        unique_together = ('school', 'code')
        ordering = ['school', 'name']

    def __str__(self):
        return f"{self.school.name} - {self.name}"


class AcademicYear(models.Model):
    """
    Academic year model.
    """
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='academic_years')
    name = models.CharField(max_length=20)  # e.g., "2023-2024"
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'academic_years'
        verbose_name = _('Academic Year')
        verbose_name_plural = _('Academic Years')
        unique_together = ('school', 'name')
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.school.name} - {self.name}"


class Term(models.Model):
    """
    Academic term/semester model.
    """
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='terms')
    name = models.CharField(max_length=50)  # e.g., "Term 1", "Semester 1"
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'terms'
        verbose_name = _('Term')
        verbose_name_plural = _('Terms')
        unique_together = ('academic_year', 'name')
        ordering = ['academic_year', 'start_date']

    def __str__(self):
        return f"{self.academic_year.name} - {self.name}"


class Holiday(models.Model):
    """
    School holidays model.
    """
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='holidays')
    name = models.CharField(max_length=100)
    date = models.DateField()
    is_recurring = models.BooleanField(default=False)  # For annual holidays
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'holidays'
        verbose_name = _('Holiday')
        verbose_name_plural = _('Holidays')
        unique_together = ('school', 'name', 'date')
        ordering = ['date']

    def __str__(self):
        return f"{self.school.name} - {self.name} ({self.date})"


class User(AbstractUser, TimeStampedModel):
    """
    Custom user model extending Django's AbstractUser.
    """
    USER_TYPE_CHOICES = [
        ('admin', 'Administrator'),
        ('teacher', 'Teacher'),
        ('staff', 'Staff'),
        ('parent', 'Parent'),
        ('student', 'Student'),
    ]

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='staff'
    )
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='users/profile_pics/', blank=True, null=True)
    is_staff_member = models.BooleanField(default=False)  # For non-teaching staff
    is_teacher = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_user_type_display()})"


class UserSchoolMembership(models.Model):
    """
    Many-to-many relationship between users and schools with roles.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='school_memberships')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='user_memberships')
    role = models.CharField(max_length=50)  # Will be linked to Role model later
    is_primary = models.BooleanField(default=False)  # Primary school for the user
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'user_school_memberships'
        verbose_name = _('User School Membership')
        verbose_name_plural = _('User School Memberships')
        unique_together = ('user', 'school')

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.school.name} ({self.role})"


class Role(models.Model):
    """
    Role/permission model for RBAC.
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'roles'
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')

    def __str__(self):
        return self.name


class Permission(models.Model):
    """
    Permission model for fine-grained access control.
    """
    name = models.CharField(max_length=100)
    codename = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    module = models.CharField(max_length=50)  # e.g., 'students', 'fees', 'attendance'
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'permissions'
        verbose_name = _('Permission')
        verbose_name_plural = _('Permissions')
        unique_together = ('module', 'codename')

    def __str__(self):
        return f"{self.module}: {self.name}"


class RolePermission(models.Model):
    """
    Many-to-many relationship between roles and permissions.
    """
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='role_permissions')
    granted_at = models.DateTimeField(auto_now_add=True)
    granted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='granted_permissions')

    class Meta:
        db_table = 'role_permissions'
        verbose_name = _('Role Permission')
        verbose_name_plural = _('Role Permissions')
        unique_together = ('role', 'permission')

    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"


class UserRoleAssignment(models.Model):
    """
    Assignment of roles to users within a school context.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='role_assignments')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_assignments')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='role_assignments')
    assigned_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_roles')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'user_role_assignments'
        verbose_name = _('User Role Assignment')
        verbose_name_plural = _('User Role Assignments')
        unique_together = ('user', 'role', 'school')

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role.name} @ {self.school.name}"


class Settings(models.Model):
    """
    System settings model.
    """
    school = models.OneToOneField(School, on_delete=models.CASCADE, related_name='settings')
    # Academic settings
    working_days = models.JSONField(default=list, help_text="List of working days (0=Monday, 6=Sunday)")
    default_date_format = models.CharField(max_length=10, default='DD-MM-YYYY')
    default_currency = models.CharField(max_length=3, default='INR')
    timezone = models.CharField(max_length=50, default='Asia/Kolkata')
    
    # Financial settings
    financial_year_start_month = models.IntegerField(default=4)  # April for Indian fiscal year
    late_fee_calculation_day = models.IntegerField(default=5)  # Day of month to calculate late fees
    
    # Notification settings
    sms_provider = models.CharField(max_length=50, blank=True)
    email_provider = models.CharField(max_length=50, blank=True)
    whatsapp_enabled = models.BooleanField(default=False)
    
    # System settings
    maintenance_mode = models.BooleanField(default=False)
    allow_self_registration = models.BooleanField(default=False)
    session_timeout_minutes = models.IntegerField(default=30)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'settings'
        verbose_name = _('Setting')
        verbose_name_plural = _('Settings')

    def __str__(self):
        return f"{self.school.name} Settings"


class AuditEvent(models.Model):
    """
    Audit trail model for tracking all important changes.
    """
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('APPROVE', 'Approve'),
        ('REJECT', 'Reject'),
        ('APPROVE_PAYMENT', 'Approve Payment'),
        ('REVERSE_PAYMENT', 'Reverse Payment'),
        ('APPROVE_REFUND', 'Approve Refund'),
        # Add more as needed
    ]
    
    id = models.BigAutoField(primary_key=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='audit_events')
    campus = models.ForeignKey(Campus, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_events')
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_actions')
    actor_role = models.CharField(max_length=100, blank=True)  # Role at time of action
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES)
    entity_type = models.CharField(max_length=50)  # Model name
    entity_id = models.CharField(max_length=50)  # Stringified ID for flexibility
    previous_data = models.JSONField(null=True, blank=True)  # Previous state
    new_data = models.JSONField(null=True, blank=True)  # New state
    change_reason = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    request_id = models.CharField(max_length=100, blank=True, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audit_events'
        verbose_name = _('Audit Event')
        verbose_name_plural = _('Audit Events')
        indexes = [
            models.Index(fields=['school', 'timestamp']),
            models.Index(fields=['entity_type', 'entity_id']),
            models.Index(fields=['action_type', 'timestamp']),
            models.Index(fields=['request_id']),
        ]
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.action_type} {self.entity_type}#{self.entity_id} by {self.actor} at {self.timestamp}"


class Attachment(models.Model):
    """
    File attachment model for documents, images, etc.
    """
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='attachments')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='uploaded_attachments')
    file = models.FileField(upload_to='attachments/')
    original_filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()  # in bytes
    mime_type = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'attachments'
        verbose_name = _('Attachment')
        verbose_name_plural = _('Attachments')
        indexes = [
            models.Index(fields=['school', 'uploaded_at']),
        ]

    def __str__(self):
        return self.original_filename


class Notification(models.Model):
    """
    Notification template/model.
    """
    NOTIFICATION_TYPES = [
        ('ADMISSION_APPROVED', 'Admission Approved'),
        ('FEE_RECEIPT', 'Fee Receipt'),
        ('FEE_DUE_REMINDER', 'Fee Due Reminder'),
        ('ABSENT_STUDENT', 'Absent Student'),
        ('LEAVE_APPROVED', 'Leave Approved'),
        ('EXAM_RESULT_PUBLISHED', 'Exam Result Published'),
        ('LIBRARY_OVERDUE', 'Library Overdue'),
        ('CERTIFICATE_ISSUED', 'Certificate Issued'),
        ('PAYROLL_AVAILABLE', 'Payroll Available'),
        ('GENERAL_NOTICE', 'General Notice'),
        # Add more as needed
    ]
    
    CHANNELS = [
        ('IN_APP', 'In-App'),
        ('EMAIL', 'Email'),
        ('SMS', 'SMS'),
        ('WHATSAPP', 'WhatsApp'),
        ('PRINT', 'Print'),
    ]
    
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='notifications')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    channel = models.CharField(max_length=20, choices=CHANNELS)
    title = models.CharField(max_length=200)
    message = models.TextField()
    template_data = models.JSONField(default=dict, blank=True)  # Data used for templating
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.notification_type} to {self.recipient.get_full_name()}"


class NotificationDelivery(models.Model):
    """
    Tracking of notification delivery attempts.
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('DELIVERED', 'Delivered'),
        ('FAILED', 'Failed'),
        ('BOUNCED', 'Bounced'),
    ]
    
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='deliveries')
    channel = models.CharField(max_length=20, choices=Notification.CHANNELS)
    provider_message_id = models.CharField(max_length=255, blank=True)  # ID from service provider
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    attempt_count = models.PositiveIntegerField(default=0)
    last_attempt_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    failure_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notification_deliveries'
        verbose_name = _('Notification Delivery')
        verbose_name_plural = _('Notification Deliveries')
        indexes = [
            models.Index(fields=['notification', 'status']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.notification} - {self.channel} - {self.status}"


class BackgroundJobRun(models.Model):
    """
    Tracking of background job executions.
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('RUNNING', 'Running'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    job_name = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='background_job_runs')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    progress_percentage = models.PositiveIntegerField(default=0)
    result_data = models.JSONField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    triggered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='triggered_jobs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'background_job_runs'
        verbose_name = _('Background Job Run')
        verbose_name_plural = _('Background Job Runs')
        indexes = [
            models.Index(fields=['school', 'status']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.job_name} - {self.status} ({self.created_at})"


class NumberSequence(models.Model):
    """
    Model to generate sequential numbers in a thread-safe manner.
    Used for documents like application numbers, receipt numbers, etc.
    """
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='number_sequences')
    name = models.CharField(max_length=100, help_text="e.g., 'application_number', 'fee_receipt'")
    prefix = models.CharField(max_length=20, blank=True, help_text="Prefix for the generated number")
    current_value = models.PositiveBigIntegerField(default=0)
    increment_by = models.PositiveIntegerField(default=1)
    reset_period = models.CharField(
        max_length=20,
        choices=[
            ('never', 'Never'),
            ('daily', 'Daily'),
            ('monthly', 'Monthly'),
            ('yearly', 'Yearly'),
        ],
        default='never',
        help_text="When to reset the counter"
    )
    last_reset = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'number_sequences'
        verbose_name = _('Number Sequence')
        verbose_name_plural = _('Number Sequences')
        unique_together = ('school', 'name')

    def __str__(self):
        return f"{self.school.name} - {self.name}: {self.current_value}"

    def next_value(self):
        """Atomically increment and return the next value."""
        from django.db import transaction
        from django.utils import timezone
        with transaction.atomic():
            # Lock the row for update
            seq = NumberSequence.objects.select_for_update().get(pk=self.pk)
            # Check if reset is needed based on reset_period and last_reset
            today = timezone.now().date()
            if seq.reset_period == 'daily' and seq.last_reset != today:
                seq.current_value = 0
                seq.last_reset = today
            elif seq.reset_period == 'monthly' and (seq.last_reset is None or seq.last_reset.month != today.month or seq.last_reset.year != today.year):
                seq.current_value = 0
                seq.last_reset = today
            elif seq.reset_period == 'yearly' and (seq.last_reset is None or seq.last_reset.year != today.year):
                seq.current_value = 0
                seq.last_reset = today
            # Increment
            seq.current_value += seq.increment_by
            seq.save(update_fields=['current_value', 'last_reset'])
            # Return formatted number
            if seq.prefix:
                return f"{seq.prefix}{seq.current_value}"
            else:
                return str(seq.current_value)