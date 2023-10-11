import json
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from companies.models import Company
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


class IndexView(LoginRequiredMixin, ListView):
    template_name = "index.html"
    paginate_by = 10
    model = Company


class RequestProfileView(LoginRequiredMixin, View):
    def post(selft, request):
        # Validate
        try:
            json_data = json.loads(request.body)
            company_id = json_data["company_id"]
            company = Company.objects.get(pk=company_id)
        except (KeyError, ObjectDoesNotExist):
            return JsonResponse(
                {"message": "Bad request!"},
                status=400,
            )

        print(request.user, company)
        if request.user.email_verified_on is None:
            return JsonResponse(
                {
                    "message": "You need to verify your email before using this function!"
                },
                status=400,
            )

        company.run_profile_request_flow(request)

        return JsonResponse(
            {
                "message": "The request has been sent successfully, you will receive the company profile via email when the request is approved!"
            },
            status=200,
        )


class ApprovedRequestProfileView(View):
    def get(self, request, cidb64, uidb64, token):
        arr = Company.verify_approve_profile_request_token(cidb64, uidb64, token)
        if arr:
            [company_id, user] = arr
            try:
                company = Company.objects.get(pk=company_id)
                company.send_profile_to_user_email(user)
                # return HttpResponse("The company profile request has been approved!")
                messages.success(
                    request,
                    "The company profile request has been approved!",
                )

            except ObjectDoesNotExist:
                messages.error(
                    request,
                    "The link is invalid!",
                    extra_tags="danger"
                )
        else:
            messages.error(
                request,
                "the link is invalid!",
                extra_tags="danger"
            )
        return redirect("companies:response-profile-request")


class ResponseRequestProfileView(View):
    template_name = "blank.html"

    def get(self, request):
        return render(request, self.template_name)
