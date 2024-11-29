# Generated by Django 5.1.3 on 2024-11-28 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluations',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('trader_name', models.CharField(max_length=255)),
                ('risk_level', models.CharField(choices=[('principiante', 'Principiante'), ('intermedio', 'Intermedio'), ('avanzado', 'Avanzado')], max_length=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]