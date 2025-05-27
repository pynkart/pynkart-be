from pynkauth.models import User
from pynkmail.models import UserEmailSettings

from django.db import transaction


def user_ownership_auth(user, entity) -> bool:
    if entity.UserID == user:
        return True
    return False

@transaction.atomic
def setting_create_or_set(
    *, email: str, key: str, user: User
) -> UserEmailSettings:
    settings = UserEmailSettings.objects.update_or_create(LoginEmail=email, SecretKey=key, UserID = user.id)
    return settings