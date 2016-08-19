# -*- encoding: utf-8 -*-
import os
import datetime
from django.utils import timezone

def get_resources_path():
    return os.path.join(os.path.join(os.path.join('resources',
                                                  '%s' % datetime.date.today().year),
                                     '%s' % datetime.date.today().month),
                        '%s' % datetime.date.today().day)

def get_models_path():
    return os.path.join(os.path.join(os.path.join('models',
                                                  '%s' % datetime.date.today().year),
                                     '%s' % datetime.date.today().month),
                        '%s' % datetime.date.today().day)

def utc2local(utc_st):
    if not utc_st:
        return None
    return timezone.localtime(utc_st)