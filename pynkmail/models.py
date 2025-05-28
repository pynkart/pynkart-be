from django.db import models
from pynkauth.models import AbstractUserOwnedModel

class UserEmailSettings(AbstractUserOwnedModel):
    LoginEmail = models.EmailField()
    SecretKey = models.CharField(max_length=64) # Default is encrypted using mat-mul with entered password and actual key
    MailAllowance = models.IntegerField(default=1000)
    
class UserEmailFormats(AbstractUserOwnedModel):
    FormatID = models.AutoField(primary_key=True)
    FormatTitle = models.CharField(max_length=64)
    FormatBody = models.CharField(max_length=2048)
    

    
    