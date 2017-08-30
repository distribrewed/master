from __future__ import absolute_import, unicode_literals

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "distribrewed.settings.settings")

# noinspection PyUnresolvedReferences
from distribrewed_core.celery import *
# noinspection PyUnresolvedReferences
import distribrewed_core.tasks
