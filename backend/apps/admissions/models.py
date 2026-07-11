from django.db import models
from django.core.validators import RegexValidator
from apps.core.models import TimeStampedModel, School, Campus, Attachment

class Enquiry(TimeStampedModel):
    """Initial enquiry from prospective students/parents"""
    ENQUIRY_SOURCE_CHOICES = [
        ('website', 'Website'),
        ('referral', 'Referral'),
        ('social_media', 'Social Media'),
        ('advertisement', 'Advertisement'),
        ('walk_in', 'Walk-in'),
        ('other', 'Other'),
    ]

    ENQUIRY_STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('follow_up', 'Follow-up Required'),
        ('converted', 'Converted to Application'),
        ('lost', 'Lost'),
    ]

    # Contact Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    phone_number = models.CharField(validators=[phone_regex], max_length=17)

    # Enquiry Details
    enquiry_date = models.DateField(auto_now_add=True)
    source = models.CharField(max_length=20, choices=ENQUIRY_SOURCE_CHOICES)
    status = models.CharField(
        max_length=20,
        choices=ENQUIRY_STATUS_CHOICES,
        default='new'
    )
    preferred_course = models.CharField(max_length=200)
    expected_start_date = models.DateField()
    notes = models.TextField(blank=True)

    # Follow-up
    last_contacted = models.DateTimeField(null=True, blank=True)
    next_follow_up = models.DateTimeField(null=True, blank=True)
    contacted_by = models.ForeignKey(
        'core.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='enquiries_contacted'
    )
    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        related_name='enquiries',
        default=1
    )
    campus = models.ForeignKey(
        Campus,
        on_delete=models.PROTECT,
        related_name='enquiries',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.enquiry_date}"

    class Meta:
        ordering = ['-enquiry_date']
        verbose_name = 'Enquiry'
        verbose_name_plural = 'Enquiries'

class Application(TimeStampedModel):
    """Formal application for admission"""
    APPLICATION_STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('waitlisted', 'Waitlisted'),
        ('deferred', 'Deferred'),
    ]

    # Link to enquiry (optional - some applications may come directly)
    enquiry = models.OneToOneField(
        Enquiry,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='application'
    )
    school = models.ForeignKey(
        School,
        on_delete=models.PROTECT,
        related_name='applications',
        default=1
    )
    campus = models.ForeignKey(
        Campus,
        on_delete=models.PROTECT,
        related_name='applications',
        null=True,
        blank=True
    )

    # Application Details
    application_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )
    application_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=APPLICATION_STATUS_CHOICES,
        default='submitted'
    )

    # Applicant Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(
        max_length=10,
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    )
    email = models.EmailField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    address = models.TextField()

    # Academic Information
    previous_school = models.CharField(max_length=200, blank=True)
    previous_class_grade = models.CharField(max_length=50, blank=True)
    percentage_marks = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Percentage in last qualifying examination"
    )

    # Course Selection
    applied_for_class = models.CharField(max_length=50)  # e.g., "Grade 1", "Year 7"
    preferred_stream = models.CharField(max_length=100, blank=True)  # e.g., "Science", "Commerce"

    # Documents (references to Attachment)
    birth_certificate = models.ForeignKey(
        'core.Attachment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='application_birth_certificates'
    )
    transfer_certificate = models.ForeignKey(
        'core.Attachment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='application_transfer_certificates'
    )
    mark_sheets = models.ForeignKey(
        'core.Attachment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='application_mark_sheets'
    )
    address_proof = models.ForeignKey(
        'core.Attachment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='application_address_proofs'
    )

    # Relational Parent/Guardian Information
    father = models.ForeignKey(
        'students.Guardian',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='father_applications'
    )
    mother = models.ForeignKey(
        'students.Guardian',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mother_applications'
    )
    primary_guardian = models.ForeignKey(
        'students.Guardian',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='guardian_applications'
    )

    # Admission Decision
    approved_by = models.ForeignKey(
        'core.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_applications'
    )
    approval_date = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # Generate application number if not set
        if not self.application_number:
            from apps.core.models import NumberSequence
            # Use the school associated with this application (if any) or fallback to school_id=1
            school_id = self.school_id if self.school_id else 1
            seq = NumberSequence.objects.get_or_create(
                school_id=school_id,
                name='application_number',
                defaults={'prefix': 'APP-', 'increment_by': 1}
            )[0]
            self.application_number = seq.next_value()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.application_number} - {self.first_name} {self.last_name}"

    class Meta:
        ordering = ['-application_date']
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
