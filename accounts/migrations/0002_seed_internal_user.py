from django.contrib.auth.hashers import make_password
from django.db import migrations


def seed_internal_user(apps, schema_editor):
    InternalUser = apps.get_model("accounts", "InternalUser")
    if not InternalUser.objects.filter(username="internal_admin").exists():
        InternalUser.objects.create(
            username="internal_admin",
            password=make_password("internal_admin"),
        )


def remove_seed_internal_user(apps, schema_editor):
    InternalUser = apps.get_model("accounts", "InternalUser")
    InternalUser.objects.filter(username="internal_admin").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_internal_user, remove_seed_internal_user),
    ]
