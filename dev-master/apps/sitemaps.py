from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.conf import settings


class StaticSitemap(Sitemap):
    def items(self):
        return [
       
            "home",
            "login",
            "logout",
            "register",
            "edit_profile",
            "edit_profile_contact_number",
            "edit_profile_shipping_address",
            "edit_bio_info",
            "change_password",
            "password_reset",
            "password_reset_done",
            "password_reset_complete",
            "contact",
            "planform",
            "About",
            "FAQ",
            "misc",
            "add_card",
            "charge",
            "TermsConditions",
            "PrivacyPolicy",
            "edit_address",
            "Paypal",
            "how-it-works-url",
            "send_issue_regarding_subscription_url",
            "schedule_call",
      

           
           
        ]

    def location(self, item):
        if isinstance(item, tuple):
            return reverse(item[0], kwargs=item[1])
        return reverse(item)

