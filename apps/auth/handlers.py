from django.dispatch import receiver
from apps.auth.signals import user_with_new_email
from apps.auth.models import Confirmation


@receiver(user_with_new_email, dispatch_uid="user_with_new_email")
def user_with_new_email_handler(sender, **kwargs):
    user = kwargs['user']

    user_just_created = kwargs.get('user_just_created', True)

    if user._email_wtc is None:
        user._email_wtc = user.email
        user.save()

    # Ckeck if exists previous confirmation:
    confs = Confirmation.objects.filter(user=user, confirmation_type=Confirmation.EMAIL)
    for c in confs:
        c.delete()

    user.generate_email_confirmation()

    user.send_confirmation_mail(user_just_created)
