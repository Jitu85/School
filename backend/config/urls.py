"""school_management URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def api_info(request):
    return JsonResponse({
        "status": "healthy",
        "name": "Smart School API",
        "version": "1.0.0"
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/info', api_info),
    path('api/info/', api_info),
    path('api/v1/auth/', include('apps.identity.urls')),
    path('api/v1/academics/', include('apps.academics.urls')),
    path('api/v1/admissions/', include('apps.admissions.urls')),
    path('api/v1/students/', include('apps.students.urls')),
    path('api/v1/attendance/', include('apps.attendance.urls')),
    path('api/v1/fees/', include('apps.fees.urls')),
    path('api/v1/accounting/', include('apps.accounting.urls')),
    path('api/v1/staff/', include('apps.staff.urls')),
    path('api/v1/payroll/', include('apps.payroll.urls')),
    path('api/v1/exams/', include('apps.exams.urls')),
    path('api/v1/library/', include('apps.library.urls')),
    path('api/v1/inventory/', include('apps.inventory.urls')),
    path('api/v1/registers/', include('apps.registers.urls')),
    path('api/v1/communication/', include('apps.communication.urls')),
    path('api/v1/documents/', include('apps.documents.urls')),
    path('api/v1/reporting/', include('apps.reporting.urls')),
    path('api/v1/audit/', include('apps.audit.urls')),
    path('api/v1/core/', include('apps.core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)