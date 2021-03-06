# Import signals in distribrewed.celery to make them work

from django.dispatch import Signal

worker_registered = Signal(providing_args=['worker_id', 'worker_info', 'worker_methods'])
worker_de_registered = Signal(providing_args=['worker_id', 'worker_info'])

handle_pong = Signal(providing_args=['worker_id'])

schedule_finished = Signal(providing_args=['worker_id', 'schedule_id'])
receive_grafana_rows = Signal(providing_args=['worker_id', 'rows'])
