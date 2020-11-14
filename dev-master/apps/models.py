from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.core.mail import EmailMessage
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
import datetime
from datetime import date
from django.core.exceptions import *
from django.db.models.signals import pre_save
from django.dispatch import receiver


# ****************************************************************
# Subscription Choices
# ****************************************************************
SUBSCRIPTION_STATUS = (
    ("Inactive", "Joined"),
    ('Pending', "Pending Admin Approval"),
    ("Active", "Approve"),
    ("Ship", "Shipment"),
    ("Approved", "Activate"),
    ("CancelSubscription", "Cancel Subscription"),
    ("7", "Cancellation Confirm"),
    ("8", "Change of Responsibility"),
    ("9", "Owner Accept Change of Responsibility"),
    

)

# ****************************************************************
# Plan Status
# ****************************************************************
PLAN_STATUS = (
    ("Inactive", "Joined"),
    ('Pending', "Pending Admin Approval"),
    ("Active", "Approve"),
    ("Decline", "Decline")

)


FIXED_SLOT_CHOICES = [(int(i), str(i)) for i in range(0, 11)]

FAMILY_SLOT_CHOICES = [(int(i), str(i)) for i in range(1, 20)]


class profileModel(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    contactNumber = models.CharField(
        max_length=14, blank=True, null=True, default='')
    paid_untill = models.DateField(null=True, blank=True)
    # shipping_address=models.CharField(max_length=100, default="" , blank=True, null=True, verbose_name="Shipping Address")
    country=models.CharField(max_length=50, default="", blank=True, null=True, verbose_name="Contry/Region")
    street_address=models.CharField(max_length=100, default="", blank=True, null=True, verbose_name="Street Address")
    apartment=models.CharField(max_length=50, default="", blank=True, null=True, verbose_name="Apt, suit. (Optional)")
    city=models.CharField(max_length=50, default="", blank=True, null=True, verbose_name="City")
    state=models.CharField(max_length=50, default="", blank=True, null=True, verbose_name="State")
    zip_code=models.CharField(max_length=50, default="", blank=True, null=True, verbose_name="Zip Code")
    

    def __str__(self):
        return self.contactNumber

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contact'

    def get_contact(self):
        return self.contactNumber


class category(models.Model):
    Name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, default="")

    class Meta:
        verbose_name="Mobile Carrier"
        verbose_name_plural="Mobile Carrier"

    
    def __str__(self):
        return self.Name

     # ****************************************************************
     # Get all plans for a specific category (Approved)
     # ****************************************************************
    def get_plans(self):
        return self.plan_set.all().filter(status="Active").order_by('total_slots')


    # ****************************************************************
    # Get all plans that do not have a leave request
    # ****************************************************************
    def get_plans_not_on_leave(self):
        return self.plan_set.all().filter(status="Active").filter(leaveRequest=False).order_by('total_slots')


# ****************************************************************
# Plan Names for a specific category
# ****************************************************************
class CategoryPlanName(models.Model):
    category = models.ForeignKey(category, on_delete= models.CASCADE, verbose_name="Mobile Carrier")
    name = models.CharField(verbose_name="Plan Name", max_length = 100, default="", blank=False, null=True)
    data = models.CharField(max_length = 100, verbose_name = "Data", blank = True, default = '', null = True)
    Hotspot = models.CharField(max_length = 100, verbose_name = "Hotspot", blank = True, default = "", null = True)
    streaming = models.CharField(max_length = 100, verbose_name = "Streaming", blank = True, default = "", null = True)
    international_TD = models.CharField(max_length = 100, verbose_name = "Internatonal Texting and Data", blank = True, default = "", null = True)
    Talk_Text = models.CharField(max_length = 100, verbose_name = "Talk & Text", blank = True, default = "", null = True)
    
    
    plan_price = models.CharField(verbose_name="Plan Fixed Price", default='', blank=True, null=True, max_length=6)

    class Meta:
        verbose_name="Mobile Carrier Plan Names"
        verbose_name_plural="Mobile Carrier Plan Names"
    
    def __str__(self):
        return f"{self.category}:{self.name}"


class plan(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    category = models.ForeignKey(category, on_delete=models.CASCADE, verbose_name="Mobile Carrier")
    family_name = models.CharField(max_length=150)
    plan_name = models.CharField(max_length=150)
    # number_of_open_slots = models.IntegerField(
    #     blank=False, default=0, null=False)
    familySize = models.IntegerField(verbose_name="Currently Family Size",
        blank=False, default=0, null=False,
        choices = FAMILY_SLOT_CHOICES
)
    monthly_payment_date = models.CharField(max_length=150)
    currently_monthly_payment_per_line = models.CharField(max_length=150)
    total_slots = models.IntegerField(
        verbose_name="Total Available Slots", blank=False, null=False, default=0, choices=FIXED_SLOT_CHOICES)
    
    linkWeb = models.URLField(
        max_length=200, blank=True, default='', null=True)
    currentFamilySize = models.IntegerField(verbose_name="Total Joiners",
                                            blank=True,
                                            null=True,
                                            default=0,
                                            help_text="The currently users who join plan."
                                            )
    notes = models.TextField(max_length=500, blank=True, default='', null=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, verbose_name="Plan Status",
                              default="Inactive", blank=False, null=False, choices=PLAN_STATUS)
    
    leaveRequest = models.BooleanField(verbose_name="Leave Request", default=False)
    
    class Meta:
        verbose_name="Plan Owners"
        verbose_name_plural="Plan Owners"

    def __str__(self):
        return "{c}-{p}-{f}".format(c = self.category.Name,p = self.plan_name,f = self.family_name)

    # ****************************************************************
    # Get Category ID
    # ****************************************************************
    def get_category_id(self):
        return category.objects.get(id=self.category.id).id

    # ****************************************************************
    # Get Plan Owner Contact Number
    # ****************************************************************

    def get_contact(self):
        try:
            return profileModel.objects.get(user=User.objects.get(username=self.user.username)).contactNumber
        except:
            return None

    # ****************************************************************
    # Subscription Objects
    # ****************************************************************
    def get_subscription_objects(self):
        return self.subscription_set.all().order_by("-created_at")

    # ****************************************************************
    # Retrieve Plan Subscription status
    # ****************************************************************
    def get_approve_subscription(self):
        try:
            return subscription.objects.get(user=User.objects.get(username=self.user.username), plan__id=self.id)
        except:
            return None

    # ****************************************************************
    # Retrive whether the current plan have available slots to subscribe
    # ****************************************************************
    def get_available_status(self):
        return True

    # ****************************************************************
    # Retrive the Subscription model for current login user and plan
    # ****************************************************************
    def get_subscription(self):
        try:
            return subscription.objects.get(user=User.objects.get(username=self.user.username), plan__id=self.id)
        except:
            return None

    def get_comments(self):
        try:
            return self.commentplan_set.all().order_by("-timestamp")
        except:
            return None



# ****************************************************************
# Plan Family Rules
# ****************************************************************
class planFamilyRules(models.Model):
    plan = models.ForeignKey(plan, on_delete=models.CASCADE)
    explanation = models.TextField(max_length=200, verbose_name="Family Rule Explanation", blank = False, null=True, default = 0)
    ruleNumber = models.IntegerField(verbose_name="Rule Number", blank=True, null=True, default=1, editable=True)

    class Meta:
        verbose_name="Plan Family Rules"
        verbose_name_plural="Plan Family Rules"
   
    def __str__(self):
        return f"{self.plan.plan_name}"


# ****************************************************************
# Plan Cancellation Rules
# ****************************************************************
class planCncellationPolicy(models.Model):
    plan = models.ForeignKey(plan, on_delete=models.CASCADE)
    explanation = models.TextField(max_length=200, verbose_name="Family Rule Explanation", blank = False, null=True, default = 0)
    ruleNumber = models.IntegerField(verbose_name="Rule Number", blank=True, null=True, default=1, editable=True)


    class Meta:
        verbose_name="Plan Cancellation Policy"
        verbose_name_plural="Plan Cancellation Policy"

    def __str__(self):
        return f"{self.plan.plan_name}"


# *****************************************************
# Subscription Model when a user joins a plan
# *****************************************************
class subscription(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    plan = models.ForeignKey(plan, on_delete=models.CASCADE)
    number_of_slots = models.IntegerField(verbose_name="Number of Slots",
                                          blank=False,
                                          null=False,
                                          default=0)
    TotalAmount = models.IntegerField(verbose_name="Total Amount",
                                      blank=False,
                                      null=False,
                                      default=0)

    created_at = models.DateField(auto_now_add=True)

    feedback = models.TextField(
        verbose_name="Feedback", max_length=500, default="", blank=True, null=True)
    status = models.CharField(max_length=20, verbose_name="Subscription Status",
                              default="Inactive", blank=False, null=False, choices=SUBSCRIPTION_STATUS)
    leaveRequest = models.BooleanField(verbose_name="Leave Request", default=False)
    device_IMEI = models.CharField(max_length=200, verbose_name="IMEI",blank=True, default="", null=True)
    subs_contact_switch = models.CharField(max_length=15, verbose_name="Switch Contact Number", blank=True, null=True, default='')
    subs_account = models.CharField(max_length=20, verbose_name="Account Number", blank=True, null=True, default='')
    subs_PIN = models.CharField(max_length=20, verbose_name="PIN Number", blank=True, null=True, default='')
    payment_contactNumber = models.CharField(max_length=15, verbose_name="Subscriber's Contact Number", blank=True, null=True, default='')
    mobile_carrier = models.CharField(max_length=100, verbose_name="Carrier", default="", blank = True, null=True)
    joining_condition = models.CharField(max_length=30, verbose_name="Joining Condition", default="", blank=True, null=True)
    area_code = models.CharField(max_length=200, verbose_name="Area Code", default='', blank=True, null=True)
    order_number = models.CharField(max_length=9, default='', verbose_name="Order Number", blank=True, null=True)
    ICCID = models.CharField(max_length=200,default = '', verbose_name="ICCID", blank=True, null=True)
    ESIM = models.CharField(max_length=200,default = '', verbose_name="ESIM/ DIGITAL SIM", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Subscription"


    def save(self, *args, **kwargs):
        if self.status == "CancelSubscription" or self.status == "7":
            self.leaveRequest = True
        else:
            self.leaveRequest = False
        super().save(*args, **kwargs)  # Call the "real" save() method.


class commentPlan(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    plan = models.ForeignKey(plan, on_delete=models.CASCADE)
    message = models.TextField(
        max_length=300, verbose_name="Commment Body", blank=False, default='', null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment By {self.user.username} on {self.plan.plan_name}"


class Api_key(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    paymentMenthod = models.CharField(max_length=150)
    customer_Id = models.CharField(max_length=150)
    subscription_ID = models.CharField(max_length=150)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

        
class Address(models.Model):
    user             = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    customer_id      = models.CharField(max_length = 150)
    B_address_line1  = models.CharField(max_length = 150)
    B_address_line2  = models.CharField(max_length = 150)
    B_City           = models.CharField(max_length = 150)
    B_State          = models.CharField(max_length = 150)
    B_Postal_code    = models.CharField(max_length = 150)
    B_Country        = models.CharField(max_length = 150)
    C_address_line1  = models.CharField(max_length = 150)
    C_address_line2  = models.CharField(max_length = 150)
    C_City           = models.CharField(max_length = 150)
    C_State          = models.CharField(max_length = 150)
    C_Postal_code    = models.CharField(max_length = 150)
    C_Country        = models.CharField(max_length = 150)

    def __str__(self):
        return self.user.username

class PayPal(models.Model):
    user            = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    email           = models.CharField(max_length=500)
    name            = models.CharField(max_length=500)
    description     = models.TextField()
    
    def __str__(self):
        return self.user



# ? Next Invoice Comming Bill
class next_estimated_Invoice_Bill(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    plan = models.ForeignKey(plan, on_delete=models.CASCADE)
    bill = models.CharField(max_length=10, verbose_name="Next Estimated Invoice Bill Amount",default="", blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}-{}-{}".format(self.user.username, self.plan.plan_name, self.bill)

class Email_Newsletter(models.Model):
    email = models.CharField(max_length=100, blank=True, null=True,default="")

    def __str__(self):
        return self.email