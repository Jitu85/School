from django.db import migrations

def seed_default_school(apps, schema_editor):
    School = apps.get_model('core', 'School')
    Campus = apps.get_model('core', 'Campus')
    NumberSequence = apps.get_model('core', 'NumberSequence')

    # Seed Default School if none exists
    school, created = School.objects.get_or_create(
        code='DEFAULT',
        defaults={
            'name': 'Smart School',
            'address': 'Default Address, City',
            'phone': '1234567890',
            'email': 'admin@smartschool.com',
            'is_active': True,
        }
    )

    # Seed Default Campus
    campus, created = Campus.objects.get_or_create(
        school=school,
        code='MAIN',
        defaults={
            'name': 'Main Campus',
            'address': 'Default Address, City',
            'is_active': True,
        }
    )

    # Seed Application Number Sequence
    # We use name='application_number' and prefix='' (empty string)
    # so next_value() returns just integers that we pad to 6 digits on save.
    NumberSequence.objects.get_or_create(
        school=school,
        name='application_number',
        defaults={
            'prefix': '',
            'current_value': 0,
            'increment_by': 1,
            'reset_period': 'never',
        }
    )

def remove_default_school(apps, schema_editor):
    School = apps.get_model('core', 'School')
    School.objects.filter(code='DEFAULT').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_numbersequence'),
    ]

    operations = [
        migrations.RunPython(seed_default_school, reverse_code=remove_default_school),
    ]
