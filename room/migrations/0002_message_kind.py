# Generated by Django 5.0.6 on 2024-06-05 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("room", "0001_Room"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="kind",
            field=models.IntegerField(choices=[(1, "Message"), (2, "File")], default=1),
        ),
    ]