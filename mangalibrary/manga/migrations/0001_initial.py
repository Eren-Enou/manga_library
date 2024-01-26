# Generated by Django 5.0.1 on 2024-01-26 02:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Manga",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("author", models.CharField(max_length=255)),
                ("artist", models.CharField(blank=True, max_length=255, null=True)),
                ("genres", models.CharField(max_length=255)),
                ("status", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
                ("cover_image_url", models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Chapter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("number", models.FloatField()),
                ("title", models.CharField(blank=True, max_length=255, null=True)),
                ("url", models.URLField()),
                ("release_date", models.DateField()),
                (
                    "manga",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="chapters",
                        to="manga.manga",
                    ),
                ),
            ],
            options={
                "ordering": ["number"],
            },
        ),
    ]