# --- Imports ---
from pynkauth.models import User
from pynkmail.models import UserEmailSettings, UserEmailFormats
from django.db import transaction
from celery import shared_task
import smtplib
from time import sleep


# --- Aux Function ---
def user_ownership_auth(user, entity) -> bool:
    if entity.UserID == user:
        return True
    return False


# --- DB Transactions ---
@transaction.atomic
def setting_create_or_set(
    *, email: str, key: str, user: User
) -> UserEmailSettings:
    settings = UserEmailSettings.objects.update_or_create(LoginEmail=email, SecretKey=key, UserID = user)
    return settings


@transaction.atomic
def format_create(
    *, title: str, body: str, user: User
) -> UserEmailFormats:
    format = UserEmailFormats.objects.create(FormatTitle = title, FormatBody = body, UserID = user)
    return format


# --- Celery Tasks ---
@shared_task
def validate_gkey_task(
    *, email: str, key: str
):
    smtp_server = smtplib.SMTP(host="smtp.gmail.com", port=587) # TODO replace with a global server
    smtp_server.starttls()
    try:
        smtp_server.login(user=email, password=key)
        return True
    except Exception as e:
        print(e)
        return False
    