import logging
import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "amplifier_test.settings")
app = Celery("amplifier_test")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

LOG_FILE_PATH = "logs/celery.log"
LOG_DIR = os.path.dirname(LOG_FILE_PATH)

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE_PATH), logging.StreamHandler()],
)
