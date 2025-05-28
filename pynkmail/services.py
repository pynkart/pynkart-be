# --- Imports ---
from pynkauth.models import User
from pynkmail.models import UserEmailSettings, UserEmailFormats
from django.db import transaction
from celery import shared_task
import smtplib
import pandas as pd


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
    
    
@shared_task
def validate_df_task(
    dt: str
):
    try:
        df = pd.read_csv(dt)
        if "email" in df.columns:
            return True, df
        return False, None
    except Exception as e:
        return False, None
    

@shared_task
def validate_format_task(
    df: pd.DataFrame, format: UserEmailFormats
):
    pass
    # prune for [] substrings to prevent forced crashes
    
    
@shared_task
def send_email_task(
    format: UserEmailFormats, df: pd.DataFrame, user: User
):
    # Create and start server
    router_server = smtplib.SMTP(host="smtp.gmail.com", port=587)
    router_server.starttls()
    
    # Attempt login
    settings = UserEmailSettings.objects.get(UserID=user)
    try:
        router_server.login(user=settings.LoginEmail, password=settings.SecretKey)
        print(format.FormatTitle)
    except Exception as e:
        print(settings.LoginEmail + " login failed.")
    
    # Drop all empty "unnamed columns"
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    columns = df.columns.values
    
    columns_to_zip = [df[col] for col in columns]
    
    # TODO fix this hardcoded limit by using pruning methods above (this accounts for all columns pre-prune)
    if len(columns) > 8:
        raise Exception("Too many columns")
    
    # Iterate through all rows
    for row_values in zip(*columns_to_zip):
        msg = format.FormatBody
        # Not O(n^2) nested loop due to column never being bigger than 8
        for i in range(0, len(columns)):
            msg = msg.replace(f"[{columns[i]}]", row_values[i])
        print(msg)
        
        
def format_message(
    columns, values, body: str
):
    # Not O(n^2) nested loop due to column never being bigger than 8
    for i in range(0, len(columns)):
        body = body.replace(f"[{columns[i]}]", values[i])
    return body
        
    