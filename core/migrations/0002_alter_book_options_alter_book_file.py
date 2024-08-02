# Generated by Django 5.0.7 on 2024-08-02 19:36

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="book",
            options={"verbose_name": "Book", "verbose_name_plural": "Books"},
        ),
        migrations.AlterField(
            model_name="book",
            name="file",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="books/",
                validators=[
                    core.validators.validate_file_extension,
                    core.validators.validate_file_size,
                ],
            ),
        ),
    ]