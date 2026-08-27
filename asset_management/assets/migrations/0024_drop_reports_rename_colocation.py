import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("assets", "0023_notification_subscribers"),
    ]

    operations = [
        migrations.DeleteModel(name="ReportableField"),
        migrations.DeleteModel(name="ReportableModel"),
        migrations.DeleteModel(name="FieldBehavior"),
        migrations.RenameModel(old_name="RayaDataCenterVM", new_name="ColocationVM"),
        migrations.AlterModelOptions(
            name="colocationvm",
            options={
                "ordering": ["environment", "name"],
                "verbose_name": "Colocation VM",
                "verbose_name_plural": "Colocation VMs",
            },
        ),
        migrations.AlterField(
            model_name="colocationvm",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="created_colocation_vms",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
