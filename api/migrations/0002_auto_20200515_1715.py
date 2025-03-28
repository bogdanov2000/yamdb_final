# Generated by Django 3.0.5 on 2020-05-15 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(name="category", options={"ordering": ["-id"]},),
        migrations.AlterModelOptions(name="comment", options={"ordering": ["-id"]},),
        migrations.AlterModelOptions(name="genre", options={"ordering": ["-id"]},),
        migrations.AlterModelOptions(name="review", options={"ordering": ["-id"]},),
        migrations.AlterModelOptions(name="title", options={"ordering": ["-id"]},),
        migrations.AlterField(
            model_name="title",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="categories",
                to="api.Category",
            ),
        ),
    ]
