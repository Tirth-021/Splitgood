from django.core import mail

from Splitgood import settings


def send_email(email, uuid, group_name):
    uri = f"http://127.0.0.1:8000/invited-register/{uuid}"
    connection = mail.get_connection()
    subject = "Welcome to Split-good "
    message = "We are glad to have you here! \n" \
              "You are invited to join " \
              + group_name + "\nYou can signup on " + uri
    email = mail.EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        connection=connection,
    )
    email.send()