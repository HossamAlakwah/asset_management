from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("assets", "0022_api_refactor_split_endpoints"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notificationrecipient",
            name="models_to_notify",
            field=models.ManyToManyField(
                blank=True,
                related_name="subscribers",
                to="assets.notificationconfig",
            ),
        ),
    ]
