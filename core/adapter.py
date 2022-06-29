from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from exposeee_api.settings import CORS_ALLOWED_ORIGINS


class CustomAccountAdapter(DefaultAccountAdapter):

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        ctx = {
            "user": emailconfirmation.email_address.user,
            "current_site": CORS_ALLOWED_ORIGINS[0],
            "key": emailconfirmation.key,
        }
        if signup:
            email_template = "account/email/email_confirmation_signup"
        else:
            email_template = "account/email/email_confirmation"
        self.send_mail(email_template, emailconfirmation.email_address.email, ctx)
