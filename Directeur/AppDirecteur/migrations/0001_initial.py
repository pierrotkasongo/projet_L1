# Generated by Django 4.2.3 on 2023-07-27 11:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('AppAuth', '0001_initial'),
        ('AppAdmin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classe', models.CharField(max_length=100)),
                ('ecoleId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppAdmin.ecole')),
            ],
        ),
        migrations.CreateModel(
            name='Eleve',
            fields=[
                ('userId', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('classeId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppDirecteur.classe')),
            ],
        ),
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateDebut', models.DateField()),
                ('dateFin', models.DateField()),
                ('status', models.CharField(default='en cours', max_length=50)),
                ('ecoleId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppAdmin.ecole')),
            ],
        ),
        migrations.CreateModel(
            name='Candidat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('electionId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppDirecteur.election')),
                ('eleveId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppDirecteur.eleve')),
            ],
        ),
    ]
