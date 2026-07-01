from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0019_carechatsession_carechatmessage_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="carechatsession",
            name="care_image",
            field=models.FileField(blank=True, null=True, upload_to="care_chat_images"),
        ),
        migrations.AddField(
            model_name="carechatsession",
            name="visual_analysis_details",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="carechatsession",
            name="visual_analysis_label",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name="carechatsession",
            name="visual_analysis_summary",
            field=models.TextField(blank=True),
        ),
    ]
