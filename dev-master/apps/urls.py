from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.conf import settings
from django.conf.urls import url
from django.urls import path
urlpatterns = [
    url(r'^$',views.home, name = "home"),
    url(r'login/', views.login_user, name = 'login'),
    url(r'^logout/$', views.logout_user, name= "logout"),
    url(r'^register/$', views.register_user, name= "register"),
    url(r'^profile/$', views.edit_profile, name = "edit_profile"),
    # Edit Contact Number through AJAX
    path("profile/edit-contact-number/", views.edit_contact_number, name="edit_profile_contact_number"),
    # Edit Shipping Address through AJAX
    path("profile/edit-shipping-address/", views.edit_shippingaddress, name="edit_profile_shipping_address"),
    #Edit Profile First Name, Last Name through Ajax
    path("profile/edit-profile/", views.edit_profile_info, name="edit_bio_info"),
    #Password Change URL............
    url(r'^change_password/$', views.change_password, name = "change_password"),
    #password Reset URLS...........
    path('password_reset/', PasswordResetView.as_view(), name='password_reset' ),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #Email Confirm URLs.....
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    #Contact Us Page ...
    url(r'^contact/$', views.contact, name="contact"),
    # ****************************************************************
    # Plan Add Form
    # ****************************************************************
    url(r'^planform/$', views.planFormView, name="planform"),
    # ****************************************************************
    # Plan Edit Form
    # ****************************************************************
    url(r'^planeditform/(?P<id>\d+)/$', views.planEditFormView, name="planeditform"),
    # ****************************************************************
    # Plan Detail Page + Plan Join Page
    # ****************************************************************
    path('join-plan/<int:category_id>/<int:plan_id>/', views.Join_A_Plan, name="Join"),
    # ****************************************************************
    # Cancel a plan
    # ****************************************************************
    path('cancel-a-plan/<int:plan_id>', views.DeletePlan, name="DeletePlan"),
    # ****************************************************************
    # Cancel plan Request
    # ****************************************************************
    path("cancel-request/<int:cat_id>/<int:plan_id>", views.leaveFamily, name="leaveFamily" ),
    # ****************************************************************
    # Subscription Cancel Request
    # ****************************************************************
    path('cancel-subscription/<int:plan_id>/<int:sub_id>/', views.Cancel_A_Plan, name="cancel"),
    # ********************************************************************
    path('ship-subscription/<int:user_id>/<int:plan_id>/<int:sub_id>/', views.ShipSubscription, name="shipSubs"),
    # ****************************************************************
    # Accept Subsription Cancel Request
    # ****************************************************************
    path('delete-subscription/<int:plan_id>/<int:sub_id>', views.Delete_Subscription, name="Delete"),
    # ****************************************************************
    # Approve a subscription for a user
    # ****************************************************************
    path('approve-subscription/<int:user_id>/<int:plan_id>/<int:sub_id>/', views.ApproveSubscription, name="Approve"),
    # ****************************************************************
    # Disapprove a subscription for a user
    # ****************************************************************
    path('disapprove-subscription/<int:user_id>/<int:plan_id>/<int:sub_id>/', views.DisapproveSubscription, name="Disapprove"),
    # ****************************************************************
    # Edit a subscription
    # ****************************************************************
    path("edit-a-subscription/<int:plan_id>/<int:sub_id>/", views.EditSubscription, name="EditSubscription"),
    # ****************************************************************
    # Subscription Detail View
    # ****************************************************************
    path('detail-view-subscription/<int:plan_id>/<int:sub_id>', views.Detail, name="Details"),
    # ****************************************************************
    # About Us
    # ****************************************************************
    path('about-us', views.About, name="About"),
    # ****************************************************************
    # FAQ
    # ****************************************************************
    path('FAQ', views.FAQ, name="FAQ"),
    # ****************************************************************
    # Plan Comment View
    # ****************************************************************
    path('plan-comment/<int:plan_id>/', views.planCommentView, name="comment_plan"),
    # ********************************************************************
    # ****************************************************************
    # Payment Method Goes Here
    # ****************************************************************
    path('profile-payment', views.misc, name="misc"),
    url(r'^edit_card/(?P<id>\w+)/$', views.edit_card, name="edit_card"),
    url(r'^delete_payment/(?P<id>\w+)/$', views.delete_payment, name="delete_payment"),
    url(r'^make_default/(?P<id>\w+)/$', views.make_default, name="make_default"),
    path('add_card', views.add_card, name="add_card"),
    path('charge', views.charge, name="charge"),
    # ****************************************************************
    # Terms of use Page
    # ****************************************************************
    path("terms-of-use", views.TermsConditions, name="TermsConditions"),
    # ****************************************************************
    # Privacy Policy
    # ****************************************************************
    path("privacy-policy", views.PrivacyPolicy, name="PrivacyPolicy"),
    #****************** Billing ANd Shipping Address ******************
    path("edit_address", views.edit_address, name="edit_address"),
    #****************** PayPal ************************************
    path("Paypal", views.Paypalview, name="Paypal"),
    # How it works page
    path("How-It-Works", views.HowItWorks, name="how-it-works-url"),
    # Device Compatibility Issue Contact
    path("Device-Compatibility-Issue-Contact/<int:cat_id>/<int:plan_id>/", views.DeviceCompatibilityIssue, name="DeviceCompatibilityIssue_URL"),
    # Send Issue regarding payment during subscription from plan detail page
    path("send-issue-regarding-payment", views.send_issue_regarding_subscription, name="send_issue_regarding_subscription_url"),
    # Schedule Call with Calendly
    path("schedule_call",views.schedule_call,name='schedule_call'),


    
    url(r'^send/$', views.send, name='send'),



]

