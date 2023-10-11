from django.urls import path
from authentication.views import SignupView, EmailVerificationView

app_name = "authentication"

urlpatterns = [
    path("sign-up", SignupView.as_view(), name="signup"),
    path(
        "email-verification/<uidb64>/<token>",
        EmailVerificationView.as_view(),
        name="email-verification",
    ),
]
