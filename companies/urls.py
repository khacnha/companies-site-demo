from django.urls import path
from companies.views import (
    IndexView,
    RequestProfileView,
    ApprovedRequestProfileView,
    ResponseRequestProfileView,
)

app_name = "companies"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path(
        "profile-request",
        RequestProfileView.as_view(),
        name="profile-request",
    ),
    path(
        "profile-request/approved/<cidb64>/<uidb64>/<token>",
        ApprovedRequestProfileView.as_view(),
        name="approved-profile-request",
    ),
    path(
        "profile-request/response",
        ResponseRequestProfileView.as_view(),
        name="response-profile-request",
    ),
]
