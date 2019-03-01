# Generated by Django 2.1.4 on 2019-03-01 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0005_auto_20190225_1732'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProblemCatagory',
        ),
        migrations.AlterField(
            model_name='commitrecord',
            name='cost_memory',
            field=models.IntegerField(default=-1, verbose_name='内存消耗'),
        ),
        migrations.AlterField(
            model_name='commitrecord',
            name='cost_time',
            field=models.IntegerField(default=-1, verbose_name='时间消耗'),
        ),
    ]
