import sys, requests
import json
import stripe
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import *
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.mail import (send_mail, EmailMessage)
from django.conf import settings
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
from django.core import serializers

#################################################################################
import sendgrid
import os
from sendgrid.helpers.mail import *

from django.core.mail import EmailMultiAlternatives

sg = sendgrid.SendGridAPIClient(
    api_key='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')
from_email = Email("futuresoftcode@gmail.com")
from .models import *
stripe.api_key = settings.STRIPE_SECRET_KEY
##################################################################################

# Circledin Support Email ID
SUPPORT_EMAIL = settings.CIRCLEDIN_SUPPORT_EMAIL
# ****************************************************************
# Home Page View
# ****************************************************************
def home(request):
    form = planForm()
    error = None
    if request.method == "POST" and request.is_ajax:
        form = planForm(request.POST)
        try:
            if form.is_valid():
                new = form.save(commit=False)
                new.user = request.user
                new.familySize = request.POST['familySize']
                new.status = "Pending"
                new.save()
                form.save()
                build_link = str(settings.SITE_REDIRECT_ORIGINAL) + str(reverse("edit_profile"))
                subject = 'Circledin - Nexts steps on plan creation'
                content = render_to_string('EmailTemplates/Add_Plan.html', {
                    'user': new.user,
                    'build_link' : build_link,
                    'plan_name' : new.plan_name,
                    'family_name' : new.family_name,
                    'carrier_name' : new.category
                })
                email = EmailMessage(subject, content, to=[
                                     new.user.email])
                email.send()
                build_link = str(settings.SITE_REDIRECT_ORIGINAL) + str(reverse("admin:apps_plan_change", args = [new.id]))
                content = f"Plan Details Link : {build_link}"
                email = EmailMessage("New Circle Activation", content, to=[SUPPORT_EMAIL])
                email.send()
                return JsonResponse(json.loads( json.dumps( {"instance": 'success'})), status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Usename or password may have been entered incorrectly."}, status=400)
    else:        
        value = plan.objects.all().filter(status="Active").filter(leaveRequest=False)
        if request.GET.get("category"):
            if request.GET.get("category") == "All":
                categories = category.objects.all()
            else:
                categories = category.objects.filter(Name=request.GET['category'])
        else:
            categories = category.objects.all()
        context={
            'value': value, 'categories': categories,  'form': form, 'error': error, 'filters': category.objects.all(), 
        }
        return render(request, 'music/home.html',context )




# ****************************************************************
# Login User View
# ****************************************************************
def login_user(request):
    if request.method != 'POST' :
        return redirect("home")
    elif request.is_ajax and request.method == "POST":
        secret_key = settings.RECAPTCHA_SECRET_KEY
        data = {
            'response': request.POST.get('g-recaptcha-response'),
            'secret': secret_key
        }
        resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result_json = resp.json()
        if not result_json.get('success'):
            return JsonResponse({"error": "User is a robot" }, status=400)
        else:
            form = loginForm(request.POST)
            valuenext = request.POST.get('next')
            if form.is_valid():
                try:
                    u = User.objects.get( Q(email__iexact = form.cleaned_data['username']) )
                    user = authenticate(
                        request, username=u.username, password=form.cleaned_data['password'])
                    if user is not None:
                        login(request, user)
                        if len(valuenext) != 0 and valuenext is not None:
                            return JsonResponse(json.loads( json.dumps( {"instance": valuenext})), status=200)
                        else:
                            return JsonResponse(json.loads( json.dumps( {"instance": reverse("home")})), status=200)
                    else:
                        return JsonResponse({"error": "Email or password may have been entered incorrectly."}, status=400)
                except Exception as e:
                    return JsonResponse({"error": "Email or password may have been entered incorrectly."}, status=400)
            else:
                return JsonResponse({"error": form.errors}, status=400)
    return JsonResponse({"error": ""}, status=400)

# ****************************************************************
# Logout User View
# ****************************************************************
def logout_user(request):
    logout(request)
    return redirect('home')


# ****************************************************************
# User Registration View
# ****************************************************************
def register_user(request):
    if request.method != 'POST':
        return redirect("home")
    elif request.is_ajax and request.method == "POST":
        secret_key = settings.RECAPTCHA_SECRET_KEY
        data = {
            'response': request.POST.get('g-recaptcha-response'),
            'secret': secret_key
        }
        resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result_json = resp.json()
        if not result_json.get('success'):
            return JsonResponse({"error": "User is a robot" }, status=400)
        else:
            form = registerForm(request.POST)
            form_2 = profileInformForm(request.POST)
            try:
                if form.is_valid() & form_2.is_valid():
                    user = form.save(commit=False)
                    user.is_active = False
                    user.username = form.cleaned_data['email']
                    user.set_password(form.cleaned_data['password2'])
                    user.email = form.cleaned_data['email']
                    user.save()
                    profile = profileModel.objects.create(user=user)
                    profile.contactNumber = form_2.cleaned_data['contactNumber']
                    profile.save()
                    current_site = get_current_site(request)
                    valuenext = request.POST.get('next')
                    if len(valuenext) == 0 or valuenext is None:
                        valuenext = None
                    if valuenext is not None:
                        build_link = str(settings.SITE_REDIRECT_ORIGINAL) + str(reverse("activate",args=[urlsafe_base64_encode(force_bytes(user.pk)), account_activation_token.make_token(user)])) + str("?next=") + str(valuenext)
                    else:
                        build_link = str(settings.SITE_REDIRECT_ORIGINAL) + str(reverse("activate",args=[urlsafe_base64_encode(force_bytes(user.pk)), account_activation_token.make_token(user)]))
                    content = render_to_string('music/acc_active_email.html', {
                        'user': user,
                        'build_link' : build_link
                    })
                    subject = 'Circledin - Action Required: Verify your email address'
                    to_email = user.email
                    email = EmailMultiAlternatives(subject, content, to=[to_email])
                    email.attach_alternative(content, "text/html")
                    email.send()
                    return JsonResponse(json.loads( json.dumps( {"instance": f'An email verification has been sent to "{ to_email }"'})), status=200)
                else:
                    # print(form.errors,  form_2.errors)
                    if form.errors:
                        return JsonResponse({"error": form.errors }, status=400)
                    elif form_2.errors:
                        return JsonResponse({"error": form_2.errors }, status=400)
                    return JsonResponse({"error": form.errors }, status=400)
            except Exception as e:
                return JsonResponse({"error": {"profile":"User with that information already exists"}}, status=400)
            return JsonResponse({"error": ""}, status=400)

# ****************************************************************
# User Email Vrefication View
# ****************************************************************
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        subject = 'A new User has been registered'
        content = f'A new user has been registerd\nDetails of the newly registered as follows:\nName:{user.first_name} {user.last_name}\nEmail Address:{user.email}'
        email = EmailMessage(subject, content, to=[SUPPORT_EMAIL])
        email.send()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        try:
            n = request.GET.get("next", None)
            if n is not None:
                return redirect(n)
            else:
                return redirect('home')
        except:
            return redirect('home')
    else:
        messages.warning(request, "Invalid Activation Link")
        return redirect("login")

# ****************************************************************
# Profile View
# ****************************************************************
@login_required()
def edit_profile(request):
    template_name= "Landkit/user_profile.html"
    obj = plan.objects.filter(
    user=User.objects.get(username=request.user.username))
    objS = subscription.objects.filter(
        user=User.objects.get(username=request.user.username)
    ).order_by('-number_of_slots')
    categories = category.objects.all().order_by("-Name")
    A = []
    C = {}
    for i in obj:
        if str(i.category.Name) in C.keys():
            C[str(i.category.Name)].append(i)
        else:
            C[str(i.category.Name)] = [i]
    customer = None
    invoice  = None
    invoices  = None
    upcoming = None
    try:
        profile = profileModel.objects.get(user=request.user)
    except profileModel.DoesNotExist:
        profile = profileModel.objects.create(user=request.user)
        profile.save()
    if request.method != 'POST':
        form = EditProfileForm(instance=request.user)
        form_2 = EditprofileInformForm(instance=profile)
        try:
            customer = Api_key.objects.filter(user=request.user)
            if len(customer) != 0:
                customer = customer[0]
                invoice = stripe.Invoice.list(limit=10, customer=customer.customer_Id)
                invoices = (invoice.data)
                upcoming = stripe.Invoice.upcoming(customer=customer.customer_Id)
        except:
            customer = None
            invoice  = None
            invoices  = None
            upcoming = None
    else:
        form_2 = EditprofileInformForm(request.POST, instance=profile)
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid() and form_2.is_valid():
            form.save()
            form_2.save()
            return redirect(reverse('edit_profile'))
    context = {
        'form': form,
        'profile': profile,
        'form_2': form_2,
        'edit_profile': True,
        'upcoming': upcoming,
        'invoices': invoices,
        'customer': customer,
        'obj': obj,
        'categories': categories,
        'C': C,
        'objS': objS,
         
    }
    return render(request, template_name, context)

# ****************************************************************
# Change Password View
# ****************************************************************
@login_required()
def change_password(request):
    if request.method != 'POST':
        form = PasswordChangeForm(user=request.user)
    else:
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(reverse('profile'))
    context={
        'form': form, 'change_password_section': True, 
    }
    return render(request, 'music/change_password.html', context )

# ****************************************************************
# Contact Form
# ****************************************************************
def contact(request):
    if request.method != 'POST':
        form = contactForm()
    else:
        form = contactForm(request.POST)
        secret_key = settings.RECAPTCHA_SECRET_KEY
        data = {
            'response': request.POST.get('g-recaptcha-response'),
            'secret': secret_key
        }
        resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result_json = resp.json()
        if not result_json.get('success'):
            pass
        else:
            if form.is_valid():
                subject = 'Contact Us'
                build_link = str(settings.SITE_REDIRECT_ORIGINAL) + str(reverse("home"))
                content = render_to_string('EmailTemplates/Contact_Us.html', {
                        'first_name': request.POST['userName'] ,
                        'email': request.POST['email'] ,
                        'build_link' : build_link,
                        'message' : request.POST['body']
                    })
                email = EmailMessage(subject, content, to=[request.POST['email'],SUPPORT_EMAIL])
                email.send()
                context = {
                    'form': contactForm(),
                    'send_successfull_contact': True,
                }
                try:
                    if request.POST.get("next", None):
                        messages.warning(request, "Email Send")
                        return redirect(request.POST.get("next"))
                    else:
                        return render(request, 'Landkit/contact-v3.html', context)
                except :
                    return render(request, 'Landkit/contact-v3.html', context)
    context = {
        'form': form,
    }
    return render(request, 'Landkit/contact-v3.html', context)

# ****************************************************************
# Add a New Plan Form (Request from a separate page)
# ****************************************************************
@login_required
def planFormView(request):
    form = planForm()
    if request.method == 'POST':
        form = planForm(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.user = request.user
            new.familySize = request.POST['familySize']
            new.status = "Pending"
            new.save()
            form.save()
            # current_site = get_current_site(request)
            build_link = str(settings.SITE_REDIRECT_ORIGINAL)  + str(reverse("admin:apps_plan_change", args=[new.id]))
            subject = 'New Plan [Alert]'
            content = f"Details of the new plan as follows:\n"
            content += f"Plan Creator Name : {new.user.username}\n"
            content += f"Plan Name : {new.plan_name}\n"
            content += f"Plan Family Name : {new.family_name}\n"
            content += f"Plan Category : {new.category}\n"
            content += f"Plan Creation Timestamp : {new.created}\n"
            content += f"Plan Details Link\n"
            content += str(build_link)
            email = EmailMessage(subject, content, to=[SUPPORT_EMAIL])
            email.send()
            messages.success(
                request, "Plan has been added to your plan list and has been sent to the Admin for revisions.")
            return redirect('edit_profile')
    context = {
        'form': form,
        'categories': category.objects.all(),
        'section_add_a_new_plan': True,
         
    }
    return render(request, 'app/form_plan.html', context)

# ***********************************************************
#  Plan Edit View
# ***********************************************************
@login_required
def planEditFormView(request, id):
    try:
        obj = plan.objects.get(id=id)
        if obj.user == User.objects.get(username=request.user.username):
            form = planForm(instance=obj)
            if request.method == 'POST':
                form = planForm(request.POST, instance=obj)
                # print(request.POST)
                if form.is_valid():
                    new = form.save(commit=False)
                    new.user = request.user
                    new.save()
                    form.save()
                    build_link = str(settings.SITE_REDIRECT_ORIGINAL) + str(reverse("admin:apps_plan_change", args=[new.id]))
                    subject = 'Edit Existing Plan [Alert]'
                    content = f"Details of the Edit plan as follows:\n"
                    content += f"Plan Editor Name : {new.user.username}\n"
                    content += f"Plan Name : {new.plan_name}\n"
                    content += f"Plan Family Name : {new.family_name}\n"
                    content += f"Plan Category : {new.category}\n"
                    content += f"Plan Updated Timestamp : {timezone.now()}\n"
                    content += f"Plan Details Link\n"
                    content += f"{str(build_link)}\n"
                    email = EmailMessage(subject, content, to=[
                                         SUPPORT_EMAIL])
                    email.send()
                    return redirect('edit_profile')
            context = {
                'form': form,
                'object': obj,
                'list_plans_section': True,
                'categories': category.objects.all(),
                 
            }
            return render(request, 'app/form_edit_plan.html', context)
        else:
            return render(request, 'app/error.html')
    except Exception as e:
        return render(request, 'app/error.html')

# ****************************************************************
# Join A Subscription (Join Plan) -> Subscribe to a Plan (Without Payment)
# ****************************************************************
def Join_A_Plan(request, category_id, plan_id):
    try:
        if request.user.is_authenticated:
            try:
                profile = profileModel.objects.get(user = User.objects.get(username = request.user.username))
            except :
                profile = None
        else:
            profile = None
        c = category.objects.get(id=category_id)
        p = plan.objects.get(id=plan_id, category=c)
        familyRules = planFamilyRules.objects.filter(plan = p)
        CncellationPolicy = planCncellationPolicy.objects.filter(plan = p)
        template_name = "app/join.html"
        context = {
            'slots': [i for i in range(1, p.total_slots + 1)],
            'plan': p,
            'total': len([i for i in range(1, p.total_slots + 1)]),
            'Plan_Join_Plan_Details' : True,
            'familyRules':familyRules,
            'CncellationPolicy' : CncellationPolicy,
            'profile' : profile,
            'objects' : subscription.objects.all().count(),
             
        }
        return render(request, template_name, context)
    except (plan.DoesNotExist, category.DoesNotExist, subscription.DoesNotExist):
        # return render(request, 'app/error.html')
        return redirect("home")
    except:
        return redirect("home")

# ****************************************************************
# Send Request to cancel a subscription for a plan
# ****************************************************************
@login_required
def Cancel_A_Plan(request,  plan_id, sub_id):
    if request.method != "POST":
        return render(request, 'app/error.html')
    try:
        p = plan.objects.get(id=plan_id)
        s = subscription.objects.get(
            id=sub_id, plan=p, user=User.objects.get(username=request.user.username))
        try:
            subject = 'Request to leave plan - {Mobile_Carrier} - {Plan_Name} - {Family_Name}'.format(Mobile_Carrier = p.category.Name, Plan_Name = p.plan_name,Family_Name = p.family_name)
            content = render_to_string('EmailTemplates/Leave_A_Plan.html', {
                    'user': s.user,
                })
            email = EmailMessage(subject, content, to=[s.user.email,SUPPORT_EMAIL])
            email.send()
            p.total_slots = p.total_slots + int(s.number_of_slots)
            p.currentFamilySize -= 1
            p.save()
            s.leaveRequest = True
            s.status="CancelSubscription"
            s.save()
            return redirect("edit_profile")
        except:
            return redirect("edit_profile")
    except (subscription.DoesNotExist, plan.DoesNotExist):
        return render(request, 'app/error.html')
    except :
        return redirect("edit_profile")


# ****************************************************************
# Accept Subscription Cancel Request
# ****************************************************************
@login_required
def Delete_Subscription(request, plan_id, sub_id):
    if request.method != "GET":
        return render(request, 'app/error.html')
    else:
        try:
            p = plan.objects.get(id=plan_id, user=User.objects.get(
                username=request.user.username))
            s = subscription.objects.get(id=sub_id, plan=p)
            subject = 'Subscription Alert [Subscription Cancel Request Approved]'
            content = f"""A request to cancel a subscription has been approved.\n
                    Following are the subscription details\n
                    Subscription user: {s.user}\n
                    Subscription Plan: {s.plan.plan_name}\n
                    Subscription Number of Slots: {s.number_of_slots}\n
                    Subscription Total Amount: {s.TotalAmount}\n
                    Subscription Timestamp: {s.created_at}\n
                    Reason/Feedback:\n
                    {s.feedback}\n"""
            to_email = (s.user.email, p.user.email)
            email = EmailMessage(subject, content, to=[
                                 to_email, SUPPORT_EMAIL])
            s.delete()  # Delete Subscription
            email.send()
            return redirect("edit_profile")
        except :
            return redirect("edit_profile")



# ****************************************************************
# Approve a subscription
# ****************************************************************
@login_required
def ApproveSubscription(request, user_id, plan_id, sub_id):
    try:
        p = plan.objects.get(user=User.objects.get(
            username=request.user.username), id=plan_id)
        s = subscription.objects.get(
            user=User.objects.get(id=user_id), id=sub_id, plan=p)
        s.status = "Active"
        s.save()
        link_build = str(settings.SITE_REDIRECT_ORIGINAL) +  str(reverse("edit_profile"))
        # TODO : If Process is Existing and for verizon:
        if s.joining_condition == "Existing Customer" and p.category.Name == "Verizon":
            context={
                's_first_name' : s.user.first_name,
                'Plan_Owner_First_Name' : p.user.first_name,
                'Plan_Owner_Last_Name' : p.user.last_name,
                'Plan_Owner_Email_Address' : p.user.email,
                'Mobile_Carrier' : p.category.Name,
                'Plan_Name' : p.plan_name
            }
            content = render_to_string("EmailTemplates/Approve_Subscription_Verizon.html", context)
        # TODO : If Process is Existing and for verizon:
        elif s.joining_condition == "Existing Customer" and ( p.category.Name == "T-Mobile" or p.category.Name == "AT&T" ):
            context={
                's_first_name' : s.user.first_name,
                'Plan_Owner_First_Name' : p.user.first_name,
                'Plan_Owner_Last_Name' : p.user.last_name,
                'Plan_Owner_Email_Address' : p.user.email,
                'Mobile_Carrier' : p.category.Name,
                'Plan_Name' : p.plan_name
            }
            content = render_to_string("EmailTemplates/Approve_Subscription_ATT_and_T.html", context)
        # TODO : If Process is New Number or Switch Number 
        else:
            context={
                'link_build' : link_build,
                'first_name' : s.user.first_name,
                'carrier_name' : p.category.Name,
                'plan_name' : p.plan_name,
                'family_name' : p.family_name,
                'order_number' : s.order_number
            }
            content = render_to_string("EmailTemplates/Approve_Subscription.html", context)
        email = EmailMessage('Circledin - You have been approved!', content, to=[
                             s.user.email])
        email.send()
        return redirect("edit_profile")
    except :
        return render(request, 'app/error.html')


# ****************************************************************
# Disapprove a subscription
# ****************************************************************
@login_required
def DisapproveSubscription(request, user_id, plan_id, sub_id):
    try:
        p = plan.objects.get(user=User.objects.get(
            username=request.user.username), id=plan_id)
        s = subscription.objects.get(
            user=User.objects.get(id=user_id), id=sub_id, plan=p)
        s.status = "Inactive"
        s.save()
        subject = 'Subscription Alert'
        current_site = get_current_site(request)
        # link_build = str(settings.SITE_REDIRECT_ORIGINAL) +  str(reverse("Details", args=[plan_id, s.id]))
        link_build = str(settings.SITE_REDIRECT_ORIGINAL) +  str(reverse("edit_profile"))
        to_email = (s.user.email)
        content = f"A Subscription has been disapproved.Kindly visit the following link to see details.\n\t{link_build}"
        email = EmailMessage(subject, content, to=[
                             to_email, SUPPORT_EMAIL])
        email.send()
        return redirect("edit_profile")
    except :
        return render(request, 'app/error.html')

# ****************************************************************
# Edit a Subscription
# ****************************************************************
@login_required
def EditSubscription(request, plan_id, sub_id):
    try:
        p = plan.objects.get(id=plan_id)
        s = subscription.objects.get(
            user=User.objects.get(
                username=request.user.username
            ),
            plan=p
        )
        if request.method == "POST":
            s.number_of_slots = request.POST['number_of_slots']
            s.TotalAmount = int(
                p.currently_monthly_payment_per_line) * int(request.POST['number_of_slots'])
            s.save()
            p.save()
            subject = 'Subscription Alert'
            current_site = get_current_site(request)
            link_build = str(settings.SITE_REDIRECT_ORIGINAL) + str(reverse("Details", args=[plan_id, s.id]))
            to_email = (p.user.email)
            content = f"A Subscription has been modified.Kindly visit the following link to see details.\n\t{link_build}"
            email = EmailMessage(subject, content, to=[
                                 to_email, SUPPORT_EMAIL])
            email.send()
            return redirect("edit_profile")
        else:
            template_name = "app/edit_subscription.html"
            context = {
                'slots': [i for i in range(1, p.total_slots + 1)],
                'plan': p,
                'subs': s,
                'total': len([i for i in range(1, p.total_slots + 1)]),
                 
            }
            return render(request, template_name, context)

    except (plan.DoesNotExist, category.DoesNotExist):
        return render(request, 'app/error.html')
    except :
        return redirect("edit_profile")

# ****************************************************************
# Subscription Detail View
# ****************************************************************
@login_required
def Detail(request, plan_id, sub_id):
    try:
        p = plan.objects.get(id=plan_id)
        s = subscription.objects.get(plan=p, id=sub_id)
        if s.user == User.objects.get(username=request.user.username) or p.user == User.objects.get(username=request.user.username):
            template_name = "app/detail.html"
            context = {
                'plan': p,
                'subs': s,
                 
            }
            return render(request, template_name, context)
    except (plan.DoesNotExist, category.DoesNotExist):
        return render(request, 'app/error.html')
    except :
        return redirect("edit_profile")



# ****************************************************************
# About Us
# ****************************************************************
def About(request):
    template_name = 'Landkit/About_v3.html'
    context = {
    }
    return render(request, template_name, context)

# ****************************************************************
# FAQ
# ****************************************************************
def FAQ(request):
    template_name = 'app/FAQs_v3.html'
    context = {
    }
    return render(request, template_name, context)

# ****************************************************************
# Request to delete a plan
# ****************************************************************
@login_required
def DeletePlan(request, plan_id):
    try:
        p = plan.objects.get(id=plan_id, user=User.objects.get(
            username=request.user.username))
        try:
            content = f"A request has been to cancel a plan from a {request.user.username} with the following details\n"
            content += f"Plan Owner : {request.user.username}\n"
            content += f"Plan Name : {p.plan_name}\n"
            content += f"Plan category : {p.category}\n"
            try:
                subject = 'Plan Alert [Cancel Request]'
                build_link = str(settings.SITE_REDIRECT_ORIGINAL) +  str(reverse("admin:apps_plan_change", args=[p.id]))
                content += "\nDetails Following Link\n"
                content += f"{build_link}"
                email = EmailMessage(subject, content, to=[
                                     SUPPORT_EMAIL])
                email.send()
                return redirect("edit_profile")
            except :
                return redirect("edit_profile")
        except :
            return redirect("edit_profile")
    except :
        return render(request, 'app/error.html')


# ****************************************************************
# Plan Comment Add View
# ****************************************************************
@login_required
def planCommentView(request, plan_id):
    try:
        p = plan.objects.get(id=plan_id)
        if request.method != "POST":
            return redirect(reverse("Join", args=[
                p.category.id,
                p.id
            ]))
        else:
            form = planCommentForm(request.POST)
            if form.is_valid():
                try:
                    new = form.save(commit=False)
                    new.user = request.user
                    new.plan = p
                    new.save()
                    form.save()
                    return redirect(reverse("Join", args=[
                        p.category.id,
                        p.id
                    ]))
                except :
                    return redirect(reverse("Join", args=[
                        p.category.id,
                        p.id
                    ]))
            else:
                return redirect(reverse("Join", args=[
                    p.category.id,
                    p.id
                ]))
    except :
        return render(request, 'app/error.html')


# ****************************************************************
# Terms and Conditions
# ****************************************************************
def TermsConditions(request):
    template_name = 'Landkit/terms-of-service.html'
    context = {
         
    }
    return render(request, template_name, context)


# ****************************************************************
# Privacy Policy
# ****************************************************************
def PrivacyPolicy(request):
    template_name = 'app/privacy.html'
    context = {
         
    }
    return render(request, template_name, context)


# ****************************************************************
# Leave Plan Family by plan owner
# ****************************************************************
@login_required
def leaveFamily(request,  cat_id, plan_id):
    try:
        c = category.objects.get(id=cat_id)
        p = plan.objects.get(id=plan_id, user=User.objects.get(
            username=request.user.username))
        subject = 'Plan Alert [Request to Cancel]'
        current_site = get_current_site(request)
        build_link = str(settings.SITE_REDIRECT_ORIGINAL) +  str(reverse("admin:apps_plan_change", args=[p.id]))
        content =  f"A request to cancel a plan has been made from {request.user.email}"
        content += "\nDetails Following Link\n"
        content += f"{build_link}"
        email = EmailMessage(subject, content, to=[SUPPORT_EMAIL])
        email.send()
        p.leaveRequest = True
        p.save()
        return redirect("edit_profile")
    except :
        return render(request, 'app/error.html')


# ***********************************************************************
# Join A Plan (With Payment)
# ***********************************************************************
@csrf_exempt
def charge(request):
    # secret_key = settings.RECAPTCHA_SECRET_KEY
    # data = {
    #     'response':  json.loads(request.body)["Gresponse"],
    #     'secret': secret_key
    # }
    # resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    # result_json = resp.json()
    # if not result_json.get('success'):
    #     return JsonResponse({"error": "User is a robot" }, status=400)
    bot = 'bot'
    if bot == 'bot':
        if request.method == 'POST':
            data = json.loads(request.body)
            category_id = data['category_id']
            plan_id = data['plan_id']
            paymentMethod = data['payment_method']
            card = data['card']
            details = data['details']
            C_address_line1 = data['C_address_line1']
            C_address_line2 = data['C_address_line2']
            C_City = data['C_City']
            C_State = data['C_State']
            C_Postal_code = data['C_Postal_code']
            C_Country = data['C_Country']
            finger_1, finger_2 = None, None

            # ****************************************************************************
            # Customer Instance Creation
            # ****************************************************************************
            # ? API Database to check customer is brand new or only instance exists or multiple instance exists for the same customer
            try:
                # ! If customer is old and only have one instance...
                customer = Api_key.objects.get(
                    user = User.objects.get(username = request.user.username)
                )
            # ! If Customer is brand new...
            except Api_key.DoesNotExist:
                try:
                    customer = stripe.Customer.create(
                        payment_method=stripe.PaymentMethod.retrieve(paymentMethod),
                        email=request.user.email,
                        description='About Payment Plan',
                        phone=details['phone'],
                        name=details['name'],
                        shipping={
                            'name':details['name'],
                            'address':{
                                'city':C_City,
                                'line1':C_address_line1, 
                                'line2':C_address_line2, 
                                'country':C_Country,
                                'postal_code':C_Postal_code, 
                                'state':C_State,
                            }
                        },
                        invoice_settings={
                                'default_payment_method': paymentMethod
                        }
                    )
                except Exception as e:
                    err_msg = "There is a problem during processing for a newly customer."
                    return JsonResponse(json.loads( json.dumps( {"error": str(err_msg)})), status=400)

            # ! If customer is old and have multiple instances...
            except Api_key.MultipleObjectsReturned:
                customer = Api_key.objects.filter(user=request.user)[0]

            except Exception as e:
                return JsonResponse(json.loads( json.dumps( {"error": str(e)})), status=400)

            # ***************************************************************************
            # Payment Method attach to a customer
            # ***************************************************************************
            # ? Attach payment method to an old customer
            try:
                finger_1 = stripe.PaymentMethod.retrieve(customer.paymentMenthod).card.fingerprint
                finger_2 = stripe.PaymentMethod.retrieve(paymentMethod).card.fingerprint
                if finger_1 != finger_2:
                    stripe.PaymentMethod.attach(
                        paymentMethod,
                        customer=customer.customer_Id,
                    )
            except Exception as e:
                try:
                    if(isinstance(customer, Api_key) is False):
                        stripe.PaymentMethod.attach(
                        paymentMethod,
                        customer=customer.id,
                        )
                    else:
                        stripe.PaymentMethod.attach(
                        paymentMethod,
                        customer=customer.customer_Id,
                        )
                except Exception as e:
                    return JsonResponse(json.loads( json.dumps( {"error": str(e)})), status=400)

            plans_products_list_ID=settings.PRODUCT_LIST_IDS
            if int(data['number_of_slots']) > 4:
                plan_1 = plans_products_list_ID[3]
            elif int(data['number_of_slots']) > 0 and int(data['number_of_slots']) <= 4:
                plan_1 = plans_products_list_ID[int(data['number_of_slots'])-1]
            try:
                if(isinstance(customer, Api_key) is False):
                    subscription_pay = stripe.Subscription.create(
                        customer=customer.id,
                        expand=['latest_invoice.payment_intent'],
                        items=[
                            {
                            'plan': plan_1,
                            },
                        ]
                    )
                else:
                    subscription_pay = stripe.Subscription.create(
                        customer=customer.customer_Id,
                        expand=['latest_invoice.payment_intent'],
                        items=[
                            {
                            'plan': plan_1,
                            },
                        ]
                    )
            except Exception as e:
                return JsonResponse(json.loads( json.dumps( {"error": str(e)})), status=400)

            # ! If customer is old and only have one instance...
            try:
                customer = Api_key.objects.get(
                    user = User.objects.get(username = request.user.username)
                )
            # ! If Customer is brand new...
            except Api_key.DoesNotExist:
                try:
                    Api_key.objects.create(user=request.user,paymentMenthod=paymentMethod,customer_Id=customer.id,
                    subscription_ID=subscription_pay.id)
                except Exception as e:
                    return JsonResponse(json.loads( json.dumps( {"error": str(err_msg)})), status=400)

            # ! If customer is old and have multiple instances...
            except Api_key.MultipleObjectsReturned:
                customer = Api_key.objects.filter(user=request.user)[0]
            except Exception as e:
                return JsonResponse(json.loads( json.dumps( {"error": str(e)})), status=400)
            try:
                if finger_1 != finger_2:
                    if(isinstance(customer, Api_key) is False):
                        Api_key.objects.create(
                            user=request.user,
                            paymentMenthod=paymentMethod,
                            customer_Id=customer.id,
                            subscription_ID=subscription_pay.id
                        )
                    else:
                        Api_key.objects.create(
                            user=request.user,
                            paymentMenthod=paymentMethod,
                            customer_Id=customer.customer_Id,
                            subscription_ID=subscription_pay.id
                        )
            except Exception as e:
                return JsonResponse(json.loads( json.dumps( {"error": str(e)})), status=400)

            try:
                c = category.objects.get(id=category_id)
                p = plan.objects.get(id=plan_id, category=c)
                try:
                    obj, status = subscription.objects.get_or_create(
                        user=request.user,
                        plan=p
                    )
                    if status:
                        try:
                            obj.number_of_slots = data['number_of_slots']
                            obj.TotalAmount = int(
                                p.currently_monthly_payment_per_line) * int(data['number_of_slots'])
                            obj.save()
                            p.total_slots = p.total_slots - int(obj.number_of_slots)
                            p.currentFamilySize += 1
                            if p.total_slots < 0:
                                p.total_slots = 0
                            p.save()
                            obj.status = "Pending"
                            obj.device_IMEI = data['device_IMEI']
                            obj.subs_contact_switch = data['subs_contact']
                            obj.subs_account = data['subs_account']
                            obj.subs_PIN = data['subs_PIN']
                            obj.payment_contactNumber = data['phone']
                            obj.mobile_carrier = data["mobile_carrier"]
                            obj.joining_condition = data['joiningCondition']
                            obj.area_code = data['area_codes']
                            obj.save()
                            next_estimated_Invoice_Bill.objects.create(
                                user=User.objects.get(username=request.user.username),
                                plan = p,
                                bill="1000"
                            )
                            # ? Calculate Order Number
                            if p.category.Name == "Verizon":
                                obj.order_number = "CI-VZ" + str(subscription.objects.all().count())
                            elif p.category.Name == "T-Mobile":
                                obj.order_number = "CI-TM" + str(subscription.objects.all().count())
                            elif p.category.Name == "Sprint":
                                obj.order_number = "CI-SP" + str(subscription.objects.all().count())
                            elif p.category.Name == "AT&T":
                                obj.order_number = "CI-ATT" + str(subscription.objects.all().count())
                            elif p.category.Name == "Cricket":
                                obj.order_number = "CI-CR" + str(subscription.objects.all().count())
                            obj.save()
                            
                            # ? Build Profile Link
                            link_build =  str(settings.SITE_REDIRECT_ORIGINAL) +  str(reverse("edit_profile"))
                            
                            # ? Send Email to the Plan Owner
                            subject = "Circledin - You've got a new family member! Please approve!"
                            content = render_to_string('EmailTemplates/Join_A_Plan.html', {
                            'user': p.user,
                            'build_link' : link_build,
                            'carrier_name' :  c.Name,
                            'plan_name' : p.plan_name ,
                            'family_name' :  p.family_name,
                            'joining_condition' : obj.joining_condition
                            })
                            email = EmailMessage(subject, content, to=[p.user.email])
                            email.send()

                            # ? Send Email to the Subscriber 
                            subject = "Circledin - Thank you! Confirmation #" + obj.order_number
                            content = render_to_string('EmailTemplates/Subscribe_A_Plan.html', {
                                'user': obj.user,
                                'build_link' : link_build,
                                'carrier_name' :  c.Name,
                                'plan_name' : p.plan_name ,
                                'family_name' :  p.family_name,
                                'joining_condition' : obj.joining_condition,
                                'order_number' : obj.order_number
                            })
                            email = EmailMessage(subject, content, to=[obj.user.email])
                            email.send()
                            profile = profileModel.objects.get(user=User.objects.get(username = request.user.username))
                            profile.country = C_Country
                            profile.street_address = C_address_line1 
                            profile.city = C_City
                            profile.state = C_State
                            profile.zip_code = C_Postal_code
                            profile.save()
                            return JsonResponse(json.loads( json.dumps( {"success": True})), status=200)
                        except Exception as e:
                            return JsonResponse(json.loads( json.dumps( {"error": str(e)})), status=400)
                    else:
                        return JsonResponse(json.loads( json.dumps( {"error": "Subscription is already created for this user"})), status=400)
                except Exception as e:
                    return JsonResponse(json.loads( json.dumps( {"error": str(e)})), status=400)
            except Exception as e:
                return JsonResponse(json.loads( json.dumps( {"error": str(e)})), status=400)
        return JsonResponse(json.loads( json.dumps( {"success": True})), status=200)

@login_required
def misc(request):
    template_name='Landkit/user_payment.html'
    customer = None
    invoice  = None
    invoices = None
    upcoming = []
    profile = None
    card=None
    c = None
    n = None
    try:
        profile = profileModel.objects.get(user = User.objects.get(username = request.user.username))
        n = next_estimated_Invoice_Bill.objects.filter(user=User.objects.get(username=request.user.username))
    except:
        profile = None
        n = None
    try:
        customer = Api_key.objects.filter(user=request.user)
        if len(customer) != 0:
            card = stripe.PaymentMethod.list(
                customer=customer[0].customer_Id,
                type="card",
                )
            c = stripe.Customer.retrieve(customer[0].customer_Id)
            customer = customer[0]
            invoice = stripe.Invoice.list(customer = customer.customer_Id)
            invoices = (invoice.data)
            s = stripe.Subscription.list(customer = customer.customer_Id)
            for i in s:
                upcoming.append(stripe.Invoice.upcoming( subscription = i.id))

    except Exception as e:
        messages.info(request, str(e))
    context={
        'upcoming': upcoming, 
        'invoices': invoices, 
        'customer': customer, 
        "payment_tab" : True, 
        'card': card, 
        'profile' : profile,
        'c' : c,
        'n' : n
    }
    return render(request, template_name , context)


@csrf_exempt
def add_card(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        paymentMethod = data['payment_method']
        card = data['card']
        details = data['details']
        try:
            customer = Api_key.objects.get(user=request.user)
            finger_1 = stripe.PaymentMethod.retrieve(customer.paymentMenthod).card.fingerprint
            finger_2 = stripe.PaymentMethod.retrieve(paymentMethod).card.fingerprint
            if finger_1 != finger_2:
                stripe.PaymentMethod.attach(
                    paymentMethod,
                    customer=customer.customer_Id,
                )
            else:
                messages.info(request, "Requested Payment Method has already existed in your payment method list.")
        except  Api_key.DoesNotExist:
            messages.info(request, "A payment method can not be added without first any subscription.")
            # return redirect("misc")
        except Api_key.MultipleObjectsReturned:
            customer = Api_key.objects.filter(user=request.user)
            finger_1 = stripe.PaymentMethod.retrieve(customer.paymentMenthod).card.fingerprint
            finger_2 = stripe.PaymentMethod.retrieve(paymentMethod).card.fingerprint
            if finger_1 != finger_2:
                stripe.PaymentMethod.attach(
                    paymentMethod,
                    customer=customer[0].customer_Id,
                )
            else:
                messages.info(request, "Requested Payment Method has already existed in your payment method list")
        except Exception as e:
            messages.info(request, str(e))
    return render(request, 'payment/paymentupdate.html', { })


def edit_card(request, id):
    try:
        method = stripe.PaymentMethod.retrieve(id)
        values = method.billing_details
        card = (method.card)
        if request.method == 'POST':
            method = stripe.PaymentMethod.modify(
                id,
                billing_details={'name': request.POST['username'], 'email': request.POST['useremail'],
                                    'phone': request.POST['phone'], 'address': {'city': request.POST['city'], 'state': request.POST['state'], 'country': request.POST['country']}},
                card={'exp_month': request.POST['exp_month'],
                        'exp_year': request.POST['exp_year']}
            )
            return redirect("misc")
    except Exception as e:
        messages.info(request, str(e))
        return redirect("misc")

    return render(request, 'payment/retrieve.html', {'values': values, 'card': card  })


def make_default(request, id):
    try:
        customer = Api_key.objects.filter(user=request.user)
        if len(customer) != 0:
            customer = customer[0]
            stripe.Customer.modify(
                customer.customer_Id,
                invoice_settings={'default_payment_method': id}
            )
        else:
            customer  = None
            card =None
    except Exception as e:
        print(e)
        messages.info(request, str(e))
        return redirect("misc")

    return redirect("misc")

# ? **********************************************************
# ?	Delete Payment Method
# ? **********************************************************
@login_required
def delete_payment(request, id):
    try:
        customer = Api_key.objects.get(user=request.user)
        p =stripe.PaymentMethod.list(
            customer=customer.customer_Id,
            type="card",
        )
        if len(p) == 1:
            return JsonResponse(json.loads( json.dumps( {"instance": "Please add another default card before deleting this one."})), status=400)
        else:
            stripe.PaymentMethod.detach(id)
            return JsonResponse(json.loads( json.dumps( {"instance": 'Successfully deleted'})), status=200)
    except Api_key.DoesNotExist:
        return JsonResponse(json.loads( json.dumps( {"instance": "Invalid Request. Payment Method to that customer does not exists."})), status=400)
    except Api_key.MultipleObjectsReturned:
        customer = Api_key.objects.filter(user=request.user)[0]
    except Exception as e:
        return JsonResponse(json.loads( json.dumps( {"instance": str(e)})), status=400)



def edit_address(request):
    obj = Address.objects.get(user=request.user)

    form= AddressForm(instance=obj)
    if request.method=='POST':
        form=AddressForm(request.POST , instance=obj )
        if form.is_valid():
            new = form.save(commit=False)
            new.user=(request.user)
            new.customer_id=obj.customer_id

            a=stripe.Customer.modify(
            obj.customer_id,

            address={
            'line1':request.POST['B_address_line1'],
            'line2':request.POST['B_address_line2'],
            'city':request.POST['B_City'],
            'state':request.POST['B_State'],
            'postal_code':request.POST['B_Postal_code'],
            'country':request.POST['B_Country'],

        },
            shipping={
            'name':request.user.username,
            'address':{'city':request.POST['C_City'],'line1':request.POST['C_address_line1'], 'line2':request.POST['C_address_line2'], 'country':request.POST['C_Country'],'postal_code':request.POST['C_Postal_code'], 'state':request.POST['C_State'],}
        },
                )
            new.save()
            form.save()
            # print(a)
            return redirect('home')
    context={
        'form':form,
        'object':obj,
         
    }
    return render(request,'payment/edit_address.html',context)


def Paypalview(request):
    form=PayPalForm()
    if request.method=='POST':
        form=PayPalForm(request.POST)
        if form.is_valid():
            new=form.save(commit=False)
            new.user=request.user
            new.save()
            form.save()

            return redirect('home')
    return render(request,'payment/paypal.html',{'form':form, })


def convert(time):
    return datetime.utcfromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')


# Edit Contact Number by Ajax Call
def edit_contact_number(request):
    if request.method != 'POST' :
        return redirect("edit_profile")
    elif request.is_ajax and request.method == "POST":
        try:
            user  = User.objects.get(username = request.user.username)
            profile = profileModel.objects.get(user=user)
        except profileModel.DoesNotExist:
            profile = profileModel.objects.create(user=user)
            profile.save()
        form_2 = EditprofileInformForm(request.POST, instance=profile)
        if form_2.is_valid():
            form_2.save()
            # messages.success(request, "Profile has been updated successfully.")
            return JsonResponse(json.loads( json.dumps( {"contact": profile.contactNumber})), status=200)
        else:
            return JsonResponse({"error": "Invalid Contact Number."},status=400)
    else:
        return JsonResponse({"error": "Invalid Contact Number."},status=400)


# Edit Profile Info
def edit_profile_info(request):
    if request.method != 'POST' :
        return redirect("edit_profile")
    elif request.is_ajax and request.method == "POST":
        user  = User.objects.get(username = request.user.username)
        form_2 = EditProfileForm(request.POST, instance=user)
        if form_2.is_valid():
            form_2.save()
            # messages.success(request, "Profile has been updated successfully.")
            return JsonResponse(json.loads( json.dumps( {"instance": "Success"})), status=200)
        else:
            return JsonResponse({"error": "Invalid Information."},status=400)
    else:
        return JsonResponse({"error": "Invalid Invalid Information."},status=400)


# Edit Profile Info
def edit_shippingaddress(request):
    if request.method != 'POST' :
        return redirect("edit_profile")
    elif request.is_ajax and request.method == "POST":
        user  = User.objects.get(username = request.user.username)
        try:
            # print(request.POST)
            profile = profileModel.objects.get(user=user)
            # profile.shipping_address=request.POST['shipping_address']
            profile.country=request.POST['country']
            profile.street_address=request.POST['street_address']
            profile.apartment=request.POST['apartment']
            profile.city=request.POST['city']
            profile.state=request.POST['state']
            profile.zip_code=request.POST['zip_code']
            
            profile.save()
            context={
                     "country"   : profile.country,
                        "street_address": profile.street_address,
                        "apartment": profile.apartment,
                        "city": profile.city,
                        "state": profile.state,
                        "zip_code": profile.zip_code
            }
            return JsonResponse(json.loads( json.dumps(context )), status=200)
        except:
            return JsonResponse({"error": "Invalid Invalid Information."},status=400)
    else:
        return JsonResponse({"error": "Invalid Invalid Information."},status=400)



@login_required
def ShipSubscription(request, user_id,plan_id, sub_id):
    try:
        p = plan.objects.get(id=plan_id, user=User.objects.get(username=request.user.username))
        s = subscription.objects.get(id=sub_id, plan = p, user= User.objects.get(id=user_id))
        s.status = "Ship"
        s.save()
        subject = 'Your Simcard is sent!'
        content = render_to_string("EmailTemplates/SimCardSend.html", {
            'first_name' : s.user.first_name,
            'carrier_name' : p.category.Name,
            'plan_name' : p.plan_name,
            'family_name' : p.family_name,
        })
        email = EmailMessage(subject, content, to=[s.user.email])
        email.send()
        return redirect("edit_profile")
    except Exception as e:
        # print(e)
        return redirect("edit_profile")


def HowItWorks(request):
    context={         
    }
    return render(request, "Landkit/How_It_Works_Page.html", context)

@login_required
def DeviceCompatibilityIssue(request, cat_id, plan_id):
    if request.method != "POST":
        return redirect(reverse("Join", args=[cat_id, plan_id]))
    else:
        subject = 'Device Compatibility Issue'
        content = render_to_string("EmailTemplates/Device_Compatibility_Contact.html", {
            'IMEI_element': request.POST['IMEI_element'],
            'contact_email' : request.POST['contact_email'],
            'build_link' :str(settings.SITE_REDIRECT_ORIGINAL) +  str(reverse("Join", args=[cat_id, plan_id])),
            'domain' : get_current_site(request).domain,
            'mobile_carrier': category.objects.get(id=cat_id).Name
        })
        email = EmailMessage(subject, content, to=[
                                SUPPORT_EMAIL])
        email.send()
        return redirect("home")


# *********************************************************************************
# Send Issue to the Circledin support after encounter an error during subscription from a plan-detail page
@login_required
def send_issue_regarding_subscription(request):
    template_name="modals/send_issue_regarding_subscription.html"
    subject="Circledin - Issue regarding Subscription"
    content = f"User Email : {request.user.email}"
    content += f"\nIssue:"
    content += f"\n\t{request.POST['Problem_Details']}"
    content += f"\n"
    email = EmailMessage(subject, content, to=[SUPPORT_EMAIL])
    email.send()
    return render(request, template_name)


# **********************************************************************************
# Call schedule using calendly

def schedule_call(request):

    return render(request,'Landkit/schedule_call.html',{'schedule_call':True})






# Testing Email
def send(request):
    email = request.GET.get('email')
    if email and '@' in email:
        body = 'This is a test message sent to {}.'.format(email)
        send_mail('Hello', body, 'noreply@mysite.com', [email, ])
        return HttpResponse('<h1>Sent.</h1>')
    else:
        return HttpResponse('<h1>No email was sent.</h1>')


# Email Collection
def Email_Collector(request):
    if request.method != "POST":
        return redirect("home")
    else:
        email = request.POST['email']
        obj,status = Email_Newsletter.objects.update_or_create(email=email)
        obj.save()
        return redirect(request.POST["next"])

@login_required
def Join_A_Plan_Existing_Customer(request, category_id, plan_id):
    template_name="app/Join_Existing_Customer.html"
    c = category.objects.get(id=category_id)
    p = plan.objects.get(category = c, id=plan_id)
    context={
        'category' : c,
        'plan' : p,
        'objects' : subscription.objects.all().count()
    }
    return render(request, template_name,context)

@login_required
def Join_A_Plan_Get_A_New_Number(request, category_id, plan_id):
    template_name="app/Join_Get_A_New_Number.html"
    c = category.objects.get(id=category_id)
    p = plan.objects.get(category = c, id=plan_id)
    context={
        'category' : c,
        'plan' : p,
        'objects' : subscription.objects.all().count()
    }
    return render(request, template_name,context)

@login_required
def Join_A_Plan_Switch_Carrier(request, category_id, plan_id):
    template_name="app/Join_Get_Switch_Carrier.html"
    c = category.objects.get(id=category_id)
    p = plan.objects.get(category = c, id=plan_id)
    context={
        'category' : c,
        'plan' : p,
        'objects' : subscription.objects.all().count()
    }
    return render(request, template_name,context)