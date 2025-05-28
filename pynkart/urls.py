from django.contrib import admin
from django.urls import path, include
from pynkauth.apis import (
    CreateUserAPI, LoginUserAPI, GetUserDetailsAPI, LogoutUserAPI, AuthenticatedAPI
)
from pynkmail.apis import (
    SetEmailSettingsAPI, CreateEmailFormatAPI, BulkSendEmailsAPI
)

# # pynkarts patterns
# itempatterns = [
#     path("list/", ItemsListApi.as_view(), name="paginated_all_items"),
#     path("listuser/<str:username>", UserItemsListApi.as_view(), name="paginated_user_items"),
#     path("get/<int:item_code>/", ItemsGetApi.as_view(), name="select_item"),
#     path("create/", ItemsCreateApi.as_view(), name="create_item"),
#     path("delist/", ItemsDelistAPI.as_view(), name="delist_item"),
#     path("update/", ItemsUpdateAPI.as_view(), name="update_item"),
# ]

# # iph patterns
# iphpatterns = [
#     path("list/", IPHListApi.as_view(), name="paginated_all_iph"),
#     path("get/<int:order_id>/", IPHGetApi.as_view(), name="select_iph"),
#     path("create/", IPHCreateApi.as_view(), name="create_totalcost_iph"),
#     path("update/", IPHUpdateStatusApi.as_view(), name="update_status_iph"),
#     path("cancel/", IPHCancelApi.as_view(), name="cancel_iph"),
#     path("complete/", IPHCompleteApi.as_view(), name="complete_iph"),
# ]

# # ish patterns
# ishpatterns = [
#     path("get/", ISHListApi.as_view(), name="paginated_all_ish"),
#     path("get/<int:order_id>/", ISHGetApi.as_view(), name="select_iph"),
#     path("create/", ISHCreateApi.as_view(), name="create_totalprice_iph"),
# ]


# auth patterns
authpatterns = [
    path("create/", CreateUserAPI.as_view(), name="create_user"),
    path("get/<str:username>", GetUserDetailsAPI.as_view(), name="get_user"),
    path("login/", LoginUserAPI.as_view(), name="login"),
    path("logout/", LogoutUserAPI.as_view(), name="logout"),
    path("authenticated/", AuthenticatedAPI.as_view(), name="is_authenticate")
]

# mail patterns
mailpatterns = [
    path("setsetting/", SetEmailSettingsAPI.as_view(), name="set_or_create_settings"),
    path("createformat/", CreateEmailFormatAPI.as_view(), name="create_format"),
    path("sendmail/", BulkSendEmailsAPI.as_view(), name="send_email")
]

# Global patterns
urlpatterns = [
    path("admin/", admin.site.urls),
    path("mail/", include((mailpatterns, "mail"))),
    # path("items/", include((itempatterns, "items"))),
    # path("iph/", include((iphpatterns, "item_procurement_history"))),
    # path("ish/", include((ishpatterns, "item_sales_history"))),
    path("users/", include((authpatterns, "authentication")))
]