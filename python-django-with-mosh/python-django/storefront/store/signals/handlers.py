from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from store.models import Customer


@receiver(
    post_save, sender=settings.AUTH_USER_MODEL
)  # call this when user model is saved, 1st arg: signal type, 2nd arg: targeted model
def create_customer_for_new_user(sender, **kwargs):
    if kwargs["created"]:  # returns a boolean whether instance has been created
        Customer.objects.create(user=kwargs["instance"])
