from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0021_carechatsession_doctor_summary_override"),
    ]

    operations = [
        migrations.AddField(
            model_name="carechatmessage",
            name="patient_read_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="carechatmessage",
            name="sender_doctor",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="care_chat_messages_sent", to="myapp.doctor"),
        ),
    ]
