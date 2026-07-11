from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'admissions'

router = DefaultRouter()
router.register(r'enquiries', views.EnquiryViewSet, basename='enquiry')
router.register(r'applications', views.ApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),
]
