from django.urls import path
from api.views import (extract_aadhar_data,extract_pan_data,otp,otp_verification,signup,login,generate_qr,send_money,get_transaction,admin_login)
app_name="api"
urlpatterns = [
    path('extract_aadhar_data', extract_aadhar_data, name="extract_aadhar_data"),
    path('extract_pan_data', extract_pan_data, name="extract_pan_data"),
    path('otp', otp, name="otp"),
    path('otp_verification',otp_verification,name="otp_verification"),
    path('signup',signup,name="signup"),
    path('login',login,name="login"),
    path('generate_qr',generate_qr,name="generate_qr"),
    path('send_money',send_money,name="send_money"),
    path('get_transaction',get_transaction,name="get_transaction"),
    path('admin_login',admin_login,name="admin_login")
]