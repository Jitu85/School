from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from .models import (
    School, Campus, AcademicYear, Term, Holiday, User, 
    UserSchoolMembership, Role, Permission, RolePermission, 
    UserRoleAssignment, Settings, AuditEvent, Attachment,
    Notification, NotificationDelivery, BackgroundJobRun
)
from .serializers import (
    SchoolSerializer, CampusSerializer, AcademicYearSerializer, 
    TermSerializer, HolidaySerializer, UserSerializer, 
    UserSchoolMembershipSerializer, RoleSerializer, 
    PermissionSerializer, RolePermissionSerializer, 
    UserRoleAssignmentSerializer, SettingsSerializer,
    AuditEventSerializer, AttachmentSerializer,
    NotificationSerializer, NotificationDeliverySerializer,
    BackgroundJobRunSerializer
)


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'code', 'address', 'email']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Return only active schools"""
        schools = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(schools, many=True)
        return Response(serializer.data)


class CampusViewSet(viewsets.ModelViewSet):
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['school', 'is_active']
    search_fields = ['name', 'code', 'address']
    ordering_fields = ['school__name', 'name']
    ordering = ['school__name', 'name']


class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['school', 'is_current', 'is_active']
    search_fields = ['name']
    ordering_fields = ['start_date', 'end_date']
    ordering = ['-start_date']
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Return current academic year for each school"""
        school_id = request.query_params.get('school_id')
        if school_id:
            year = self.get_queryset().filter(school_id=school_id, is_current=True).first()
            if year:
                serializer = self.get_serializer(year)
                return Response(serializer.data)
            return Response(None)
        else:
            # Return current year for all schools
            years = self.get_queryset().filter(is_current=True)
            serializer = self.get_serializer(years, many=True)
            return Response(serializer.data)


class TermViewSet(viewsets.ModelViewSet):
    queryset = Term.objects.all()
    serializer_class = TermSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['academic_year', 'is_active']
    search_fields = ['name']
    ordering_fields = ['start_date', 'end_date']
    ordering = ['academic_year', 'start_date']


class HolidayViewSet(viewsets.ModelViewSet):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['school', 'date', 'is_recurring']
    search_fields = ['name', 'description']
    ordering_fields = ['date']
    ordering = ['date']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_staff', 'is_teacher', 'is_approved', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']
    ordering_fields = ['username', 'email', 'date_joined']
    ordering = ['username']
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=False, methods=['get'])
    def teachers(self, request):
        """Return only teachers"""
        teachers = self.get_queryset().filter(is_teacher=True, is_active=True)
        serializer = self.get_serializer(teachers, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def staff(self, request):
        """Return only staff members"""
        staff = self.get_queryset().filter(is_staff_member=True, is_active=True)
        serializer = self.get_serializer(staff, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a user account"""
        user = self.get_object()
        user.is_approved = True
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        """Set password for a user"""
        user = self.get_object()
        password = request.data.get('password')
        if password:
            user.set_password(password)
            user.save()
            return Response({'status': 'password set'})
        return Response({'error': 'Password required'}, status=status.HTTP_400_BAD_REQUEST)


class UserSchoolMembershipViewSet(viewsets.ModelViewSet):
    queryset = UserSchoolMembership.objects.all()
    serializer_class = UserSchoolMembershipSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'school', 'is_primary', 'is_active']
    search_fields = ['user__username', 'user__email', 'school__name']
    ordering_fields = ['joined_at']
    ordering = ['-joined_at']


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    ordering = ['name']


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['module', 'is_active']
    search_fields = ['name', 'codename', 'description']
    ordering_fields = ['module', 'name']
    ordering = ['module', 'name']


class RolePermissionViewSet(viewsets.ModelViewSet):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'permission']
    search_fields = ['role__name', 'permission__name', 'permission__codename']
    ordering_fields = ['granted_at']
    ordering = ['-granted_at']


class UserRoleAssignmentViewSet(viewsets.ModelViewSet):
    queryset = UserRoleAssignment.objects.all()
    serializer_class = UserRoleAssignmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'role', 'school', 'is_active']
    search_fields = ['user__username', 'user__email', 'role__name', 'school__name']
    ordering_fields = ['assigned_at']
    ordering = ['-assigned_at']


class SettingsViewSet(viewsets.ModelViewSet):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['school']
    search_fields = ['school__name']
    ordering_fields = ['school__name']
    ordering = ['school__name']


class AuditEventViewSet(viewsets.ReadOnlyModelViewSet):
    """Audit events are read-only"""
    queryset = AuditEvent.objects.all()
    serializer_class = AuditEventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['action_type', 'entity_type', 'school']
    search_fields = ['entity_type', 'entity_id', 'actor__username', 'change_reason']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['school', 'is_public']
    search_fields = ['original_filename', 'description']
    ordering_fields = ['uploaded_at']
    ordering = ['-uploaded_at']


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['recipient', 'notification_type', 'channel', 'is_read']
    search_fields = ['title', 'message']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Mark all notifications as read for a user"""
        user_id = request.data.get('user_id')
        if user_id:
            updated = self.get_queryset().filter(recipient_id=user_id, is_read=False).update(is_read=True)
            return Response({'updated': updated})
        return Response({'error': 'user_id required'}, status=status.HTTP_400_BAD_REQUEST)


class NotificationDeliveryViewSet(viewsets.ModelViewSet):
    queryset = NotificationDelivery.objects.all()
    serializer_class = NotificationDeliverySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['channel', 'status']
    search_fields = ['notification__title', 'provider_message_id', 'failure_reason']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


class BackgroundJobRunViewSet(viewsets.ModelViewSet):
    queryset = BackgroundJobRun.objects.all()
    serializer_class = BackgroundJobRunSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['job_name', 'school', 'status']
    search_fields = ['job_name', 'error_message']
    ordering_fields = ['created_at', 'started_at']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def running(self, request):
        """Return currently running jobs"""
        running_jobs = self.get_queryset().filter(status='running')
        serializer = self.get_serializer(running_jobs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def failed(self, request):
        """Return failed jobs"""
        failed_jobs = self.get_queryset().filter(status='failed')
        serializer = self.get_serializer(failed_jobs, many=True)
        return Response(serializer.data)