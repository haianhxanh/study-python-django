import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "storefront.settings")  # 1: module, 2: path to module

celery = Celery("storefront")  # name of celery

# where celery can find config variables
# 1 arg: go to Django conf and load settings object
# 2 arg: define namespace, all config settings should start with the value we set, in this case CELERY
celery.config_from_object("django.conf:settings", namespace="CELERY")
# instruct celery to discover tasks
celery.autodiscover_tasks()
