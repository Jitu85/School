from rest_framework import viewsets, permissions
from .models import Enquiry, Application
from .serializers import EnquirySerializer, ApplicationSerializer

class EnquiryViewSet(viewsets.ModelViewSet):
    serializer_class = EnquirySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user and user.is_authenticated:
            if user.is_superuser:
                return Enquiry.objects.all()
            # Filter enquiries to schools where the user is an active member
            user_schools = user.school_memberships.filter(is_active=True).values_list('school_id', flat=True)
            return Enquiry.objects.filter(school_id__in=user_schools)
        # Fallback for anonymous? Not allowed due to IsAuthenticated, but keep for safety
        school_id = self.request.query_params.get('school_id')
        if school_id:
            return Enquiry.objects.filter(school_id=school_id)
        return Enquiry.objects.none()

    def perform_create(self, serializer):
        # Resolve School context
        school = None
        user = self.request.user
        if user and user.is_authenticated:
            # Try to get user's primary school
            membership = user.school_memberships.filter(is_primary=True, is_active=True).first()
            if membership:
                school = membership.school

        # Fallback 1: check if school was explicitly passed in body/query
        if not school:
            school_id = self.request.data.get('school')
            if school_id:
                from apps.core.models import School
                school = School.objects.filter(id=school_id, is_active=True).first()

        # Fallback 2: fetch the default seeded school from DB
        if not school:
            from apps.core.models import School
            school = School.objects.filter(is_active=True).first()

        if not school:
            raise serializers.ValidationError({"school": "No active school context found."})

        # Resolve Campus context
        campus = None
        campus_id = self.request.data.get('campus')
        if campus_id:
            from apps.core.models import Campus
            campus = Campus.objects.filter(id=campus_id, school=school, is_active=True).first()

        serializer.save(school=school, campus=campus)


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user and user.is_authenticated:
            if user.is_superuser:
                return Application.objects.all()
            user_schools = user.school_memberships.filter(is_active=True).values_list('school_id', flat=True)
            return Application.objects.filter(school_id__in=user_schools)
        school_id = self.request.query_params.get('school_id')
        if school_id:
            return Application.objects.filter(school_id=school_id)
        return Application.objects.none()

    def perform_create(self, serializer):
        # Resolve School context
        school = None
        user = self.request.user
        if user and user.is_authenticated:
            membership = user.school_memberships.filter(is_primary=True, is_active=True).first()
            if membership:
                school = membership.school

        if not school:
            school_id = self.request.data.get('school')
            if school_id:
                from apps.core.models import School
                school = School.objects.filter(id=school_id, is_active=True).first()

        if not school:
            from apps.core.models import School
            school = School.objects.filter(is_active=True).first()

        if not school:
            raise serializers.ValidationError({"school": "No active school context found."})

        # Resolve Campus context
        campus = None
        campus_id = self.request.data.get('campus')
        if campus_id:
            from apps.core.models import Campus
            campus = Campus.objects.filter(id=campus_id, school=school, is_active=True).first()

        serializer.save(school=school, campus=campus)
