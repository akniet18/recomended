# Generated by Django 2.2.4 on 2019-10-01 03:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('review', '0005_auto_20190918_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='payment_uid',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.CreateModel(
            name='PaymentYM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created time')),
                ('order_type', models.SmallIntegerField(choices=[(0, 'Answer'), (1, 'Deletion'), (2, 'Review'), (3, 'Review and Shame board'), (4, 'Shame board')], default=2, verbose_name='Payment for')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Total amount for payment')),
                ('currency', models.PositiveIntegerField(choices=[(643, 'Rubles'), (10543, 'Test')], default=10543, verbose_name='Currency')),
                ('status', models.CharField(choices=[(0, 'Processed'), (1, 'Success'), (2, 'Fail')], default=0, max_length=15, verbose_name='Status')),
                ('payment_type', models.CharField(choices=[('PC', 'Кошелек Яндекс.Деньги'), ('AC', 'Банковская карта'), ('WM', 'Кошелек WebMoney'), ('QW', 'QIWI Wallet')], default='AC', max_length=2, verbose_name='Payment type')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments_author', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
                'ordering': ('-created_at',),
            },
        ),
    ]