from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0022_carechatmessage_sender_doctor_and_patient_read_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="carechatsession",
            name="doctor_approved_medicine",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="carechatsession",
            name="doctor_approved_summary",
            field=models.BooleanField(default=False),
        ),
    ]
