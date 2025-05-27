from django.db import models
from django.contrib.auth.models import User


class AbstractUserOwnedModel(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_index=True, default=None, null=True) # TODO DO_NOTHING IS HARD-CODED COME UP WITH SOMETHING BETTER AT SOME POINT
    class Meta:
        abstract = True
        
