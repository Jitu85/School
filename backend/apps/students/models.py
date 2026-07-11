from django.db import models
from apps.core.models import TimeStampedModel, School, Campus

class Guardian(TimeStampedModel):
    """Guardian or Parent associated with students"""
    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        related_name='guardians',
        default=1
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=17)
    occupation = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone_number})"

    class Meta:
        db_table = 'guardians'
        verbose_name = 'Guardian'
        verbose_name_plural = 'Guardians'


class Student(TimeStampedModel):
    """Student master record"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        related_name='students',
        default=1
    )
    campus = models.ForeignKey(
        Campus,
        on_delete=models.PROTECT,
        related_name='students',
        null=True,
        blank=True
    )
    admission_number = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=17, blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.admission_number} - {self.first_name} {self.last_name}"

    class Meta:
        db_table = 'students'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


class StudentGuardian(models.Model):
    """Junction table connecting Students and Guardians with relationship details"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_guardians')
    guardian = models.ForeignKey(Guardian, on_delete=models.CASCADE, related_name='student_guardians')
    relationship = models.CharField(max_length=50, help_text="e.g., Father, Mother, Uncle, Aunt")
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.first_name} - {self.guardian.first_name} ({self.relationship})"

    class Meta:
        db_table = 'student_guardians'
        verbose_name = 'Student Guardian'
        verbose_name_plural = 'Student Guardians'
        unique_together = ('student', 'guardian')
