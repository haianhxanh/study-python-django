import celery
from time import sleep
from celery import shared_task


@shared_task  # decorate with celery
def notify_customers(message):
    print("Sending 10k emails...")
    print(message)
    sleep(10)  # put function into sleep for 10s
    print("Emails were successfully sent")
