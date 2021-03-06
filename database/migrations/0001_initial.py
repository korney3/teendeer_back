# Generated by Django 3.2.8 on 2021-10-08 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GiftedChild',
            fields=[
                ('uuid', models.IntegerField(primary_key=True, serialize=False)),
                ('specialization', models.CharField(choices=[('C', 'Class'), ('A', 'Art'), ('S', 'Singer'), ('D', 'Deers')], default='C', max_length=2)),
                ('name', models.CharField(blank=True, max_length=64, null=True)),
                ('surname', models.CharField(blank=True, max_length=64, null=True)),
                ('bio', models.CharField(blank=True, max_length=512, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
