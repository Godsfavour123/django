# Keep this nullable for Student records created before matriculation numbers
# were introduced. New and updated records are required by StudentForm.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projectapp", "0004_student"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="matriculation_number",
            field=models.CharField(max_length=30, null=True, unique=True),
        ),
    ]
