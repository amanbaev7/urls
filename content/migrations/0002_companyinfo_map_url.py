from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="companyinfo",
            name="map_url",
            field=models.URLField(blank=True, verbose_name="Ссылка на карту"),
        ),
    ]
