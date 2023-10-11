from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from authentication.forms import SignupForm
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth import get_user_model


class SignupView(View):
    form_class = SignupForm
    template_name = "signup.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # create user
            user = form.save()
            # login
            login(request, user)
            # send email verification
            user.send_email_verification_email(request)
            messages.success(
                request,
                "Your Account has been created succesfully!! Please check your email to confirm your email address.",
            )

            return redirect(settings.LOGIN_REDIRECT_URL)

        return render(request, self.template_name, {"form": form})


class EmailVerificationView(View):
    def get(self, request, uidb64, token):
        User = get_user_model()
        user = User.verify_email_token(uidb64, token)
        if user:
            messages.success(
                request,
                "Thank you for your email confirmation!",
            )
            return redirect(settings.LOGIN_REDIRECT_URL)

        return HttpResponse("The link is invalid!")
