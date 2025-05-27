from pynkauth.models import User
from pynkmail.models import UserEmailSettings, UserEmailFormats

from django.db import transaction


def user_ownership_auth(user, entity) -> bool:
    if entity.UserID == user:
        return True
    return False


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