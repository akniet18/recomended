# Generated by Django 2.2.4 on 2019-09-17 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_auto_20190916_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='review',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='review_answer', to='review.Review'),
        ),
    ]
