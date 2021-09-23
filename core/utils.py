import time


def file_name(token):
    return f'exposeee_{token}_{time.strftime("%Y-%m-%d_%I-%M-%S_%p")}.xlsx'
