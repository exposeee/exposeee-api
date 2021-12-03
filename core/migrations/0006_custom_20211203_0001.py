from django.db import migrations


def split_address_field(apps, schema_editor):
    Expose = apps.get_model('core', 'Expose')
    for expose in Expose.objects.all():
        kpis = expose.data.get('kpis')
        if kpis and set(['zipcode', 'city']) - set(kpis.keys()):
            address = kpis.get('address').split(' ')
            if len(address) > 2:
               kpis['address'] = ' '.join(address[0:-2])
               kpis['zipcode'] = address[-2]
               kpis['city'] = address[-1]
            elif len(address) == 1 and address[0]:
                kpis['address'] = ''
                kpis['zipcode'] = ''
                kpis['city'] = address[0]

        expose.data['kpis'] = kpis
        expose.save()


def change_date_kpis_field(apps, schema_editor):
    Expose = apps.get_model('core', 'Expose')
    for expose in Expose.objects.all():
        kpis = expose.data.get('kpis')
        kpis['creation_date'] = kpis.pop('date')
        expose.data['kpis'] = kpis
        expose.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_exposeuser'),
    ]

    operations = [
        migrations.RunPython(split_address_field),
        migrations.RunPython(change_date_kpis_field),
    ]
