# Generated by Django 4.0.1 on 2023-01-22 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Dossier', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='T_Rectangle',
            fields=[
                ('Rect_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Rect_Name', models.CharField(max_length=100, unique=True)),
                ('Dossier_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dossier.t_dossier')),
            ],
        ),
    ]
