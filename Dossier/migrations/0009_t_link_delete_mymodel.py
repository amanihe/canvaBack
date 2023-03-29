# Generated by Django 4.0.1 on 2023-03-12 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Dossier', '0008_mymodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='T_Link',
            fields=[
                ('Link_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Link_Name', models.CharField(max_length=100)),
                ('Link_Url', models.CharField(max_length=100)),
                ('Field_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Dossier.t_field')),
            ],
        ),
        migrations.DeleteModel(
            name='myModel',
        ),
    ]