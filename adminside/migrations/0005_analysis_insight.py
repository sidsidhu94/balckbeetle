# Generated by Django 5.0 on 2024-09-10 09:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "adminside",
            "0004_delete_segment_delete_stockindex_delete_tradetype_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Analysis",
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
                ("bull_scenario", models.CharField(max_length=1000)),
                ("bear_scenario", models.CharField(max_length=1000)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("BEARISH", "Bearish"),
                            ("BULLISH", "Bullish"),
                            ("NEUTRAL", " Neutral"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "analysis",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="adminside.trade",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Insight",
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
                ("prediction", models.CharField(max_length=255)),
                ("actual", models.CharField(max_length=255)),
                (
                    "trade",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="insights",
                        to="adminside.trade",
                    ),
                ),
            ],
        ),
    ]
