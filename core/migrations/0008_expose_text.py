# Generated by Django 4.1.3 on 2022-11-07 21:14

from django.db import migrations, models


def move_text_from_json_to_text_field(apps, schema_editor):
    Expose = apps.get_model('core', 'Expose')
    for expose in Expose.objects.all():
        text = expose.data.get('text')
        if text:
            expose.text = text
            del expose.data['text']
            expose.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20211213_2142'),
    ]

    operations = [
        migrations.AddField(
            model_name='expose',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='Text'),
        ),
        migrations.RunPython(move_text_from_json_to_text_field),
    ]
