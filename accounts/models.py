from django.db import models

class UserProfile(models.Model):
    account_number = models.CharField(max_length=255, blank=True, null=True)
    address_proof = models.CharField(max_length=255, blank=True, null=True)
    address_proof_image = models.CharField(max_length=255, blank=True, null=True)
    bank_account_number = models.CharField(max_length=255, blank=True, null=True)
    bank_branch_name = models.CharField(max_length=255, blank=True, null=True)
    bank_holder_name = models.CharField(max_length=255, blank=True, null=True)
    bank_ifsc_code = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    fund_manager = models.CharField(max_length=255, blank=True, null=True)
    group = models.CharField(max_length=255, blank=True, null=True)
    id = models.AutoField(primary_key=True)  # Assuming 'id' is your primary key
    id_proof = models.CharField(max_length=255, blank=True, null=True)
    id_proof_image = models.CharField(max_length=255, blank=True, null=True)
    is_self_trading = models.CharField(max_length=255, blank=True, null=True)
    isActive = models.BooleanField(default=False) #tinyint should be boolean
    leverage = models.CharField(max_length=255, blank=True, null=True)
    margin = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    net_profit = models.CharField(max_length=255, blank=True, null=True)
    otp = models.IntegerField(blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True) #Consider hashing passwords
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    pincode = models.CharField(max_length=255, blank=True, null=True)
    referral_code = models.CharField(max_length=255, blank=True, null=True)
    referred_by = models.CharField(max_length=255, blank=True, null=True)
    security_question = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    user_type = models.CharField(max_length=255, blank=True, null=True)
    wallet_total_amount = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'user_profile'
        managed = False

    def __str__(self):
        return self.name or self.email or "User Profile"
    

from django.db import models

class Group(models.Model):
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    swap_buy = models.CharField(max_length=255)  # varchar(255)
    swap_sell = models.CharField(max_length=255) # varchar(255)
    commision = models.CharField(max_length=255) # varchar(255)
    commision_type = models.CharField(max_length=255)
    commision_value_type = models.CharField(max_length=255)
    margin = models.CharField(max_length=255) # varchar(255)
    spread = models.CharField(max_length=255) # varchar(255)
    deviation = models.CharField(max_length=255) # varchar(255)
    min_lot = models.CharField(max_length=255) # varchar(255)
    max_lot = models.CharField(max_length=255) # varchar(255)
    type = models.CharField(max_length=255)
    pips = models.CharField(max_length=255) # varchar(255)
    spread_pip = models.CharField(max_length=255) # varchar(255)
    image = models.CharField(max_length=255, blank=True, null=True) # varchar(255) nullable
    show_points = models.CharField(max_length=255) # varchar(255)
    pip_currency = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)  # datetime(6)
    updated_at = models.DateTimeField(auto_now=True)  # datetime(6)

    class Meta:
        db_table = 'group_creation'  # Specify the existing table name
        managed = False  # Tell Django not to manage this table

    def __str__(self):
        return self.name
    

# models.py
from django.db import models

class Order(models.Model):
    order_id = models.CharField(max_length=255)
    order_status = models.CharField(max_length=255)
    order_user_id = models.CharField(max_length=255)
    order_company_name = models.CharField(max_length=255)
    order_type = models.CharField(max_length=255)
    order_price = models.CharField(max_length=255)
    order_quantity = models.CharField(max_length=255)
    contract_value = models.CharField(max_length=255)
    margin = models.CharField(max_length=255)
    net_profit = models.CharField(max_length=255)
    close_price = models.CharField(max_length=255)
    swap = models.CharField(max_length=255)
    commission = models.CharField(max_length=255)
    stop_loss = models.CharField(max_length=255)
    take_profit = models.CharField(max_length=255)
    cancel_message = models.CharField(max_length=255, blank=True, null=True)
    close_message = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_order'
        managed = False

    def __str__(self):
        return f"Order #{self.order_id} - {self.order_company_name}"
    

class WithdrawalRequest(models.Model):
    user_id = models.CharField(max_length=255)
    amount = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField()  # Removed (6)
    updated_at = models.DateTimeField()  # Removed (6)

    class Meta:
        db_table = 'withdrawal_request'
        managed = False

    def __str__(self):
        return f"Withdrawal Request {self.id} - User: {self.user.name}"