from django.dispatch import Signal

user_with_new_email = Signal(providing_args=["user", "user_just_created"])
