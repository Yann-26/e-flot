# Generated by Django 5.0.4 on 2024-05-09 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='voiture',
            old_name='car_annee_fabrication',
            new_name='annee_fabrication',
        ),
        migrations.RenameField(
            model_name='voiture',
            old_name='car_codes_erreur',
            new_name='codes_erreur',
        ),
        migrations.RenameField(
            model_name='voiture',
            old_name='car_historique_maintenance',
            new_name='historique_maintenance',
        ),
        migrations.RenameField(
            model_name='voiture',
            old_name='car_kilometrage',
            new_name='kilometrage',
        ),
        migrations.RenameField(
            model_name='voiture',
            old_name='car_modele',
            new_name='modele',
        ),
        migrations.RenameField(
            model_name='voiture',
            old_name='car_numero_serie',
            new_name='numero_serie',
        ),
        migrations.RenameField(
            model_name='voiture',
            old_name='car_symptomes',
            new_name='symptomes',
        ),
        migrations.RenameField(
            model_name='voiture',
            old_name='car_transmission',
            new_name='transmission',
        ),
        migrations.RenameField(
            model_name='voiture',
            old_name='car_type_carburant',
            new_name='type_carburant',
        ),
    ]