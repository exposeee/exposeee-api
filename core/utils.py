import time
from memba_match.constants.kpis import column_translations


def file_name(token):
    return f'exposeee_{token}_{time.strftime("%Y-%m-%d_%I-%M-%S_%p")}.xlsx'


def default_data(filename):
    return {
        'kpis': {key: filename if key == 'resource' else None for key in column_translations.keys()},
        'text': '',
        'logs': '',
    }


def format_number(str_num):
    return format(str_num, ',.2f').replace(",", "X").replace(".", ",").replace("X", ".")


def format_price(str_num):
    return f'{format_number(str_num)} €'


def format_kpis(name, value):
    if not value:
        return value

    if name in ('jnkm', 'kaufpreis'):
        return format_price(value)
    elif name in ('floor_area', 'leasable_area', 'wohnflaeche', 'gewerbeflaeche', 'multiplier', 'yield'):
        return format_number(value)
    elif name == 'price_m2':
        return f'{format_price(value)}/m²'
    else:
        return value


def format_expose(expose):
    data = expose.data
    kpis = data.pop('kpis') if 'kpis' in data else {}

    return {
        'id': expose.id,
        **expose.data,
        'kpis': {name: format_kpis(name, value) for name, value in kpis.items()},
    }
