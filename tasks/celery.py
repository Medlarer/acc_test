#!/usr/bin/env python


"""
"""

from __future__ import absolute_import, unicode_literals
from celery import Celery
from ..views import Config

app = Celery('tasks',
             broker=Config.BROKER_URL,
             backend=Config.BROKER_URL,
             include=['tasks.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()