from django.contrib import admin
from api.models import Account,Otp,Transaction,Balance,Admin

# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    list_display=('name','dob','father','phone')
admin.site.register(Account,AccountAdmin)


admin.site.register(Otp)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('sender_id', 'reciever_id', 'amount','time_stamp')
admin.site.register(Transaction,TransactionAdmin)

class BalanceAdmin(admin.ModelAdmin):
    list_display = ('account_id', 'balance', )
admin.site.register(Balance,BalanceAdmin)

class AdminAdmin(admin.ModelAdmin):
    list_display=('name','dob','phone')

admin.site.register(Admin,AdminAdmin)

admin.site.site_header='Bank'
