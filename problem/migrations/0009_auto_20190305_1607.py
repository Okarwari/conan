# Generated by Django 2.1.4 on 2019-03-05 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0008_commitrecord_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commitrecord',
            name='created_time',
            field=models.DateTimeField(auto_now=True, verbose_name='提交时间'),
        ),
    ]
