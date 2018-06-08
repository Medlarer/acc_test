#!/usr/bin/env python


"""
"""

from __future__ import absolute_import, unicode_literals
from .celery import app
from acc.views import session


@app.task
def add(x, y):
    return x + y


@app.task
def data_input():
    data = session.get("user_data")
    return data