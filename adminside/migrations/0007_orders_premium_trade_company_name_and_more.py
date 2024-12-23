# Generated by Django 5.0 on 2024-09-12 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("adminside", "0006_remove_analysis_analysis_analysis_trade_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Orders",
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
            ],
        ),
        migrations.CreateModel(
            name="Premium",
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
                ("premium_amount", models.IntegerField()),
                (
                    "premium_period",
                    models.CharField(
                        choices=[("quarterly", "Quarterly"), ("monthly", "Monthly")],
                        max_length=255,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="trade",
            name="company_name",
            field=models.CharField(default=11, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="insight",
            name="actual",
            field=models.CharField(default="Not updated", max_length=255),
        ),
        migrations.AlterField(
            model_name="insight",
            name="prediction",
            field=models.CharField(default="Not updated", max_length=255),
        ),
    ]
