from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.admin import AdminSite
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from blog.models import *

class MyAdminSite(AdminSite):
    site_header = 'Circledin Admin'
    site_title  = 'Circledin'
    index_title = 'Circledin'
 
my_admin_site = MyAdminSite(name='Mobile')

class profileAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'contactNumber']
    search_fields = ['id', 'user__username', 'user__first_name', 'user__last_name', ]
    list_per_page = 10

class categoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('Name',)}


class planAdmin(admin.ModelAdmin):
    search_fields = [
        'plan_name'

    ]

    list_display = [
        'user',
        
        'category' , 
        'plan_name', 
        'family_name', 
        'total_slots', 
        'currently_monthly_payment_per_line', 
        'status'
    ]
    list_filter=[
        'category',
        'status'
    ]

    list_per_page = 10

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.method == "POST":
            # print(request.POST, object_id)
            p = plan.objects.get(id=object_id)
            # print(p)
            if request.POST['status'] == "Active":
                if p.status != "Active":
                    subject = "Circledin - Congratulations your plan is approved"
                    # ! If Mobile Carrier is Verizon
                    if p.category.Name == "Verizon":
                        content = render_to_string("EmailTemplates/Approve_plan_Verizon.html", {
                            'FirstName' : p.user.first_name,
                            'carrier_name' : p.category.Name,
                            'plan_name' : p.plan_name
                        })
                    # ! If Mobile Carrier is T-Mobiles
                    elif p.category.Name == "T-Mobile":
                        content = render_to_string("EmailTemplates/Approve_plan_T_Mobiles.html", {
                            'FirstName' : p.user.first_name,
                            'carrier_name' : p.category.Name,
                            'plan_name' : p.plan_name
                        })
                    else:
                        content = render_to_string('EmailTemplates/Approve_plan.html', {
                        'first_name': p.user.first_name ,
                        'carrier_name': p.category.Name ,
                        'plan_name' : p.plan_name,
                        'family_name' : p.family_name
                        })
                    email = EmailMessage(subject, content, to=[p.user.email])
                    email.send()
            
            if request.POST['status'] == "Decline":
                content = render_to_string("EmailTemplates/Decline_Plan_Owner_Status.html", {
                            'FirstName' : p.user.first_name,
                            'carrier_name' : p.category.Name,
                            'plan_name' : p.plan_name
                        })
                email = EmailMessage("Circledin - Decline Plan", content, to=[p.user.email])
                email.send()
        extra_context = extra_context or {}
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

class subscriptionAdmin(admin.ModelAdmin):
    list_display = ['user','plan', 'created_at', 'number_of_slots', 'status']
    list_per_page = 10

    readonly_fields = [
        'leaveRequest'
    ]

    # search_fields = [
    #     'plan_name',
    #     # 'user'
    # ]

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.method == "POST":
            # print(request.POST, object_id)
            s = subscription.objects.get(id=object_id)
            # print(p)
            build_link= str(settings.SITE_REDIRECT_ORIGINAL) +  str(reverse("edit_profile"))
            if request.POST['status'] == "Ship":
                if s.status != "Ship":
                    subject = "Your SIM card has been shipped"
                    content = render_to_string('EmailTemplates/Shipment_send.html', {
                    'user': s.user,
                    'build_link' :  build_link ,
                    'carrie_name' :  s.plan.category.Name,
                    'plan_name' : s.plan.plan_name ,
                    'family_name' :  s.plan.family_name,
                })
                    email = EmailMessage(subject, content, to=[s.user.email])
                    email.send()
            if request.POST['status'] == "Approved":
                if s.status != "Approved":
                    subject = "Your subscription has been activated"
                    content = render_to_string('EmailTemplates/Subscription_Activated.html', {
                    'first_name': s.user.first_name,
                })
                    email = EmailMessage(subject, content, to=[s.user.email])
                    email.send()
            if request.POST['status'] == "Active":
                if s.status != "Active":
                    if s.joining_condition == "Existing Customer" and s.plan.category.Name == "Verizon":
                        context={
                            's_first_name' : s.user.first_name,
                            'Plan_Owner_First_Name' : s.plan.user.first_name,
                            'Plan_Owner_Last_Name' : s.plan.user.last_name,
                            'Plan_Owner_Email_Address' : s.plan.user.email,
                            'Mobile_Carrier' : s.plan.category.Name,
                            'Plan_Name' : s.plan.plan_name
                        }
                        content = render_to_string("EmailTemplates/Approve_Subscription_Verizon.html", context)
                    elif s.joining_condition == "Existing Customer" and ( s.plan.category.Name == "T-Mobile" or s.plan.category.Name == "AT&T" ):
                        context={
                            's_first_name' : s.user.first_name,
                            'Plan_Owner_First_Name' : s.plan.user.first_name,
                            'Plan_Owner_Last_Name' : s.plan.user.last_name,
                            'Plan_Owner_Email_Address' : s.plan.user.email,
                            'Mobile_Carrier' : s.plan.category.Name,
                            'Plan_Name' : s.plan.plan_name
                        }
                        content = render_to_string("EmailTemplates/Approve_Subscription_ATT_and_T.html", context)
                    else:
                        context={
                            'link_build' : build_link,
                            'first_name' : s.user.first_name,
                            'carrier_name' : s.plan.category.Name,
                            'plan_name' : s.plan.plan_name,
                            'family_name' : s.plan.family_name,
                            'order_number' : s.order_number
                        }
                        content = render_to_string("EmailTemplates/Approve_Subscription.html", context)
                    subject = "Circledin - You have been approved!"
                    email = EmailMessage(subject, content, to=[s.user.email])
                    email.send()
        extra_context = extra_context or {}
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )


class UserAdmin(admin.ModelAdmin):
    list_display=[
        'email', 'first_name', 'last_name'
    ]
    list_per_page=10
    ordering=[
        'email'
    ]
    search_fields=[
        # 'id',
        # '__str__',
        'username',
        'first_name',
        'last_name',
        'email'
    ]

class planFamilyRulesAdmin(admin.ModelAdmin):
    autocomplete_fields = [
        'plan'
    ]
    list_display = [
        '__str__', 
        'ruleNumber'
    ]

    ordering=[
        "plan",
        "ruleNumber"
    ]


class planCncellationPolicyAdmin(admin.ModelAdmin):
    autocomplete_fields = [
        'plan'
    ]
    list_display = [
        '__str__', 
        'ruleNumber'
    ]

    ordering=[
        "plan",
        "ruleNumber"
    ]


class next_estimated_Invoice_Bill_Admin(admin.ModelAdmin):
    list_display = [
        'user',
        'plan',
        'bill'
    ]
    list_editable = [
        'bill'
    ]

class blogPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_filter=[
        'publish'
    ]
    list_per_page=10
    list_display=[
        'title',
        'user',
        'publish'
    ]

    search_fields=[
        'title'
    ]


class postCommentAdmin(admin.ModelAdmin):
    list_filter=[
        'publish'
    ]

# Related to User Profile Management
my_admin_site.register(Group, GroupAdmin)
my_admin_site.register(User, UserAdmin)
my_admin_site.register(profileModel, profileAdmin)

my_admin_site.register(category, categoryAdmin)
my_admin_site.register(plan, planAdmin)
my_admin_site.register(subscription, subscriptionAdmin)
my_admin_site.register(commentPlan)
my_admin_site.register(Api_key)
my_admin_site.register(CategoryPlanName)
my_admin_site.register(Address)
my_admin_site.register(PayPal)
my_admin_site.register(planFamilyRules, planFamilyRulesAdmin)
my_admin_site.register(planCncellationPolicy, planCncellationPolicyAdmin)
my_admin_site.register(next_estimated_Invoice_Bill, next_estimated_Invoice_Bill_Admin)

# TODO: Blog Apps Model Customizations
my_admin_site.register(blogPost, blogPostAdmin)
my_admin_site.register(postComment, postCommentAdmin)
my_admin_site.register(commentReply)