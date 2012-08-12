from django.dispatch import Signal

# A user has added a new email to his or her account.
user_added_email = Signal(providing_args=["email_address"])

# A user send activation email to her or his primary account.
user_sent_activation = Signal(providing_args=["email_address"])

# A user has activated his or her email.
user_activated_email = Signal(providing_args=["email_address"])



