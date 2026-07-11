from django.contrib import admin
from .models import Student, Guardian, StudentGuardian

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('admission_number', 'first_name', 'last_name', 'school', 'gender', 'is_active')
    list_filter = ('school', 'gender', 'is_active')
    search_fields = ('admission_number', 'first_name', 'last_name', 'email')

@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'email', 'school')
    list_filter = ('school',)
    search_fields = ('first_name', 'last_name', 'phone_number', 'email')

@admin.register(StudentGuardian)
class StudentGuardianAdmin(admin.ModelAdmin):
    list_display = ('student', 'guardian', 'relationship', 'is_primary')
    list_filter = ('relationship', 'is_primary')
    search_fields = ('student__first_name', 'student__last_name', 'guardian__first_name', 'guardian__last_name')
