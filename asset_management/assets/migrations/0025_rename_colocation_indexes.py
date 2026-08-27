from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("assets", "0024_drop_reports_rename_colocation"),
    ]

    operations = [
        migrations.RenameIndex(
            model_name="colocationvm",
            new_name="assets_colo_environ_730131_idx",
            old_name="assets_raya_environ_b43ebe_idx",
        ),
        migrations.RenameIndex(
            model_name="colocationvm",
            new_name="assets_colo_contrac_4be3a5_idx",
            old_name="assets_raya_contrac_e6cca0_idx",
        ),
        migrations.RenameIndex(
            model_name="colocationvm",
            new_name="assets_colo_renewal_b95c64_idx",
            old_name="assets_raya_renewal_539a74_idx",
        ),
    ]
