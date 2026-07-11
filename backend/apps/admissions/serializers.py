from rest_framework import serializers
from .models import Enquiry, Application

class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = '__all__'
        extra_kwargs = {
            'school': {'required': False, 'allow_null': True},
            'campus': {'required': False, 'allow_null': True},
        }

class ApplicationSerializer(serializers.ModelSerializer):
    # Enable writing flat fields from frontend forms
    father_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    father_occupation = serializers.CharField(write_only=True, required=False, allow_blank=True)
    father_phone = serializers.CharField(write_only=True, required=False, allow_blank=True)
    mother_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    mother_occupation = serializers.CharField(write_only=True, required=False, allow_blank=True)
    mother_phone = serializers.CharField(write_only=True, required=False, allow_blank=True)

    # Read-only display fields to keep frontend compatible
    father_name_display = serializers.SerializerMethodField(read_only=True)
    mother_name_display = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Application
        fields = '__all__'
        extra_kwargs = {
            'school': {'required': False, 'allow_null': True},
            'campus': {'required': False, 'allow_null': True},
            'father': {'read_only': True},
            'mother': {'read_only': True},
            'primary_guardian': {'read_only': True},
        }

    def get_father_name_display(self, obj):
        if obj.father:
            return f"{obj.father.first_name} {obj.father.last_name}".strip()
        return ""

    def get_mother_name_display(self, obj):
        if obj.mother:
            return f"{obj.mother.first_name} {obj.mother.last_name}".strip()
        return ""

    def create(self, validated_data):
        # Resolve school
        school = validated_data.get('school')
        if not school:
            from apps.core.models import School
            school = School.objects.filter(is_active=True).first()
            validated_data['school'] = school

        father_name = validated_data.pop('father_name', None)
        father_occupation = validated_data.pop('father_occupation', None)
        father_phone = validated_data.pop('father_phone', None)

        mother_name = validated_data.pop('mother_name', None)
        mother_occupation = validated_data.pop('mother_occupation', None)
        mother_phone = validated_data.pop('mother_phone', None)

        from apps.students.models import Guardian

        # Create or retrieve relational Guardian record for Father
        if father_name or father_phone:
            parts = father_name.split(' ', 1) if father_name else ['', '']
            f_name = parts[0]
            l_name = parts[1] if len(parts) > 1 else ''
            father_obj, created = Guardian.objects.get_or_create(
                school=school,
                phone_number=father_phone or '',
                defaults={
                    'first_name': f_name or 'Father',
                    'last_name': l_name,
                    'occupation': father_occupation or '',
                }
            )
            validated_data['father'] = father_obj

        # Create or retrieve relational Guardian record for Mother
        if mother_name or mother_phone:
            parts = mother_name.split(' ', 1) if mother_name else ['', '']
            m_name = parts[0]
            l_name = parts[1] if len(parts) > 1 else ''
            mother_obj, created = Guardian.objects.get_or_create(
                school=school,
                phone_number=mother_phone or '',
                defaults={
                    'first_name': m_name or 'Mother',
                    'last_name': l_name,
                    'occupation': mother_occupation or '',
                }
            )
            validated_data['mother'] = mother_obj

        return super().create(validated_data)
