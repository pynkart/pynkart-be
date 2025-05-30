# Generated by Django 5.1.5 on 2025-05-27 01:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Items",
            fields=[
                ("ItemCode", models.AutoField(primary_key=True, serialize=False)),
                ("ItemName", models.CharField(max_length=63)),
                ("ItemDescription", models.CharField(max_length=255)),
                ("ImageUrl", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "Status",
                    models.CharField(
                        choices=[("E", "Existing"), ("D", "Deleted")],
                        default="E",
                        max_length=1,
                    ),
                ),
                (
                    "UserID",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
