# Generated by Django 2.2.13 on 2020-09-28 21:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=150)),
                ('slug', models.SlugField(default='', max_length=150)),
            ],
            options={
                'verbose_name': 'Mobile Carrier',
                'verbose_name_plural': 'Mobile Carrier',
            },
        ),
        migrations.CreateModel(
            name='plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family_name', models.CharField(max_length=150)),
                ('plan_name', models.CharField(max_length=150)),
                ('familySize', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19')], default=0, verbose_name='Currently Family Size')),
                ('monthly_payment_date', models.CharField(max_length=150)),
                ('currently_monthly_payment_per_line', models.CharField(max_length=150)),
                ('total_slots', models.IntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], default=0, verbose_name='Total Available Slots')),
                ('linkWeb', models.URLField(blank=True, default='', null=True)),
                ('currentFamilySize', models.IntegerField(blank=True, default=0, help_text='The currently users who join plan.', null=True, verbose_name='Total Joiners')),
                ('notes', models.TextField(blank=True, default='', max_length=500, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Inactive', 'Joined'), ('Pending', 'Pending Admin Approval'), ('Active', 'Approve')], default='Inactive', max_length=15, verbose_name='Plan Status')),
                ('leaveRequest', models.BooleanField(default=False, verbose_name='Leave Request')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.category', verbose_name='Mobile Carrier')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Plan Owners',
                'verbose_name_plural': 'Plan Owners',
            },
        ),
        migrations.CreateModel(
            name='subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_slots', models.IntegerField(default=0, verbose_name='Number of Slots')),
                ('TotalAmount', models.IntegerField(default=0, verbose_name='Total Amount')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('feedback', models.TextField(blank=True, default='', max_length=500, null=True, verbose_name='Feedback')),
                ('status', models.CharField(choices=[('Inactive', 'Joined'), ('Pending', 'Pending Admin Approval'), ('Active', 'Approve'), ('Ship', 'Shipment'), ('Approved', 'Activate'), ('CancelSubscription', 'Cancel Subscription'), ('7', 'Cancellation Confirm'), ('8', 'Change of Responsibility'), ('9', 'Owner Accept Change of Responsibility')], default='Inactive', max_length=20, verbose_name='Subscription Status')),
                ('leaveRequest', models.BooleanField(default=False, verbose_name='Leave Request')),
                ('device_IMEI', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='IMEI')),
                ('subs_contact_switch', models.CharField(blank=True, default='', max_length=15, null=True, verbose_name='Switch Contact Number')),
                ('subs_account', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='Account Number')),
                ('subs_PIN', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='PIN Number')),
                ('payment_contactNumber', models.CharField(blank=True, default='', max_length=15, null=True, verbose_name="Subscriber's Contact Number")),
                ('mobile_carrier', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Carrier')),
                ('joining_condition', models.CharField(blank=True, default='', max_length=30, null=True, verbose_name='Joining Condition')),
                ('area_code', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Area Code')),
                ('order_number', models.CharField(blank=True, default='', max_length=9, null=True, verbose_name='Order Number')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.plan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='profileModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contactNumber', models.CharField(blank=True, default='', max_length=14, null=True)),
                ('paid_untill', models.DateField(blank=True, null=True)),
                ('country', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Contry/Region')),
                ('street_address', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Street Address')),
                ('apartment', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Apt, suit. (Optional)')),
                ('city', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='City')),
                ('state', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='State')),
                ('zip_code', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Zip Code')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contact',
            },
        ),
        migrations.CreateModel(
            name='planFamilyRules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('explanation', models.TextField(default=0, max_length=200, null=True, verbose_name='Family Rule Explanation')),
                ('ruleNumber', models.IntegerField(blank=True, default=1, null=True, verbose_name='Rule Number')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.plan')),
            ],
            options={
                'verbose_name': 'Plan Family Rules',
                'verbose_name_plural': 'Plan Family Rules',
            },
        ),
        migrations.CreateModel(
            name='planCncellationPolicy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('explanation', models.TextField(default=0, max_length=200, null=True, verbose_name='Family Rule Explanation')),
                ('ruleNumber', models.IntegerField(blank=True, default=1, null=True, verbose_name='Rule Number')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.plan')),
            ],
            options={
                'verbose_name': 'Plan Cancellation Policy',
                'verbose_name_plural': 'Plan Cancellation Policy',
            },
        ),
        migrations.CreateModel(
            name='PayPal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=500)),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='next_estimated_Invoice_Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill', models.CharField(blank=True, default='', max_length=10, null=True, verbose_name='Next Estimated Invoice Bill Amount')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.plan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='commentPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(default='', max_length=300, null=True, verbose_name='Commment Body')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.plan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryPlanName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, null=True, verbose_name='Plan Name')),
                ('data', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Data')),
                ('Hotspot', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Hotspot')),
                ('streaming', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Streaming')),
                ('international_TD', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Internatonal Texting and Data')),
                ('Talk_Text', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Talk & Text')),
                ('plan_price', models.CharField(blank=True, default='', max_length=6, null=True, verbose_name='Plan Fixed Price')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.category', verbose_name='Mobile Carrier')),
            ],
            options={
                'verbose_name': 'Mobile Carrier Plan Names',
                'verbose_name_plural': 'Mobile Carrier Plan Names',
            },
        ),
        migrations.CreateModel(
            name='Api_key',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paymentMenthod', models.CharField(max_length=150)),
                ('customer_Id', models.CharField(max_length=150)),
                ('subscription_ID', models.CharField(max_length=150)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.CharField(max_length=150)),
                ('B_address_line1', models.CharField(max_length=150)),
                ('B_address_line2', models.CharField(max_length=150)),
                ('B_City', models.CharField(max_length=150)),
                ('B_State', models.CharField(max_length=150)),
                ('B_Postal_code', models.CharField(max_length=150)),
                ('B_Country', models.CharField(max_length=150)),
                ('C_address_line1', models.CharField(max_length=150)),
                ('C_address_line2', models.CharField(max_length=150)),
                ('C_City', models.CharField(max_length=150)),
                ('C_State', models.CharField(max_length=150)),
                ('C_Postal_code', models.CharField(max_length=150)),
                ('C_Country', models.CharField(max_length=150)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
