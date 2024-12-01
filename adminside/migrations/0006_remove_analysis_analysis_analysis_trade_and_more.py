# Generated by Django 5.0 on 2024-09-10 10:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("adminside", "0005_analysis_insight"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="analysis",
            name="analysis",
        ),
        migrations.AddField(
            model_name="analysis",
            name="trade",
            field=models.ForeignKey(
                default=2,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="analysis",
                to="adminside.trade",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="tradehistory",
            name="trade",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="history",
                to="adminside.trade",
            ),
        ),
    ]
