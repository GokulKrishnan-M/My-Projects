from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0020_carechatsession_care_image_and_visual_analysis"),
    ]

    operations = [
        migrations.AddField(
            model_name="carechatsession",
            name="doctor_summary_override",
            field=models.TextField(blank=True),
        ),
    ]
