from __future__ import absolute_import, unicode_literals

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "distribrewed.settings")

# noinspection PyUnresolvedReferences
from distribrewed_core.celery import *

queue.conf.imports = [
    'masters.signals',
    'schedules.signals'
    'workers.signals',
    'workers.tasks',
]
