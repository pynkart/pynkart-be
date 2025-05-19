from pynkseller.models import Items
from pynkauth.models import User

from django.db import transaction
from django.db.models import Sum


def user_ownership_auth(user, entity) -> bool:
    if entity.UserID == user:
        return True
    return False


@transaction.atomic
def item_create(
    *, name: str, description: str, user: User
) -> Items:
    """
    """
    item = Items.objects.create(ItemName=name, ItemDescription=description, UserID=user)
    return item


# @transaction.atomic
# def item_delist(
#     *, item_code : int, user : User
# ) -> Items:
#     item = Items.objects.get(ItemCode=item_code)
#     if not user_ownership_auth(user=user, entity=item): # Checks ownership
#         return None
    
#     inv = Inventory.objects.filter(ItemCode=item_code)
#     stock = inv.aggregate(incoming=Sum("IncomingQty"), current=Sum("CurrentQty"))
    
#     # If inventory is empty, OR, if there are already no stock
#     # Inventory being empty means there has been no orders (in or out) ever
#     if (not inv) or ((stock["incoming"] == 0) and (stock["current"] == 0)): 
#         item.Status = "D"
#         item.save(update_fields=["Status"])
#         return item
#     else:
#         return None
    

# @transaction.atomic
# def item_delist_force(
#     *, item_code : int, user : User
# ) -> Items:
#     item = Items.objects.get(ItemCode=item_code)
#     if not user_ownership_auth(user=user, entity=item): # Checks ownership
#         return None
    
#     inv = Inventory.objects.filter(ItemCode=item_code)
#     stock = inv.aggregate(incoming=Sum("IncomingQty"), current=Sum("CurrentQty"))
    
    # TODO Pseudocode
    # Cancels every IPH not completed that is associated with the item (removes all incoming qty)
    # Creates an ISH equal to the current qty (if current qty is above 0)
    # Sets item to delist
    
  
@transaction.atomic
def item_update(
    *, item_code: int, name: str, description: str, image_url :str = None, user: User
) -> Items:
    item = Items.objects.get(ItemCode=item_code)
    if not user_ownership_auth(user=user, entity=item): # Checks ownership
        return None
    
    item.ItemName = name
    item.ItemDescription = description
    item.ImageUrl = image_url # Optional field, can be none
    item.save()
    
    return item
