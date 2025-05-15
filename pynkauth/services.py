from django.db import transaction

from pynkart.settings import SECRET_KEY
from pynkauth.models import UserSettings


@transaction.atomic
# TODO Add encryption for the love of god
def set_email_secrets(
    *, email: str, secret_key: str
):
    # encrypted_key = Fernet(ENCRYPTION_KEY).encrypt(secret_key)
    # print(encrypted_key)
    user_setting, _ = UserSettings.objects.update_or_create(
        AutoEmail=email,
        create_defaults={
            "AutoEmail":email,
            "AutoMailSecret":str.encode(secret_key)
        }
    )
    return user_setting
    
    
# {"email":"owentheturkey@gmail.com","secret_key":"nanuhmpkopdqlzey"}