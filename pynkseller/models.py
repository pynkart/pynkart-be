from django.db import models
from pynkauth.models import AbstractUserOwnedModel


class Items(AbstractUserOwnedModel):
    # Status Enum
    class ItemStatus(models.TextChoices):
        EXISTING = "E", "Existing"
        DELETED = "D", "Deleted"
    
    # Fields
    ItemCode = models.AutoField(primary_key=True)
    ItemName = models.CharField(max_length=63)
    ItemDescription = models.CharField(max_length=255)
    ImageUrl = models.CharField(max_length=255, null=True, blank=True)
    Status = models.CharField( # Uses the enum above, default is pending
        max_length=1,
        choices=ItemStatus.choices,
        default=ItemStatus.EXISTING
    )
    
