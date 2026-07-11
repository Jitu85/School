from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'schools', views.SchoolViewSet)
router.register(r'campuses', views.CampusViewSet)
router.register(r'academic-years', views.AcademicYearViewSet)
router.register(r'terms', views.TermViewSet)
router.register(r'holidays', views.HolidayViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'user-school-memberships', views.UserSchoolMembershipViewSet)
router.register(r'roles', views.RoleViewSet)
router.register(r'permissions', views.PermissionViewSet)
router.register(r'role-permissions', views.RolePermissionViewSet)
router.register(r'user-role-assignments', views.UserRoleAssignmentViewSet)
router.register(r'settings', views.SettingsViewSet)
router.register(r'audit-events', views.AuditEventViewSet)
router.register(r'attachments', views.AttachmentViewSet)
router.register(r'notifications', views.NotificationViewSet)
router.register(r'notification-deliveries', views.NotificationDeliveryViewSet)
router.register(r'background-job-runs', views.BackgroundJobRunViewSet)

urlpatterns = [
    path('', include(router.urls)),
]