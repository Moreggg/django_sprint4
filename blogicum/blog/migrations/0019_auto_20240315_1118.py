# Generated by Django 3.2.16 on 2024-03-15 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_auto_20240315_1117'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('-created_at',), 'verbose_name': 'категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': ('-created_at',), 'verbose_name': 'местоположение', 'verbose_name_plural': 'Местоположения'},
        ),
    ]
