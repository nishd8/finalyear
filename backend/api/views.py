from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from api.utils import   (aadhar_data_extractor,
                        old_pan_data_extractor,
                        new_pan_data_extractor,
                        send_otp,verify_otp,
                        create_Account,
                        get_Account_by_phone,
                        generate_qr_by_acc,
                        create_transaction,
                        get_transactions,
                        get_admin)

@api_view(['POST','GET'])
def extract_aadhar_data(request):
    if(request.method == 'GET'):
        return Response('Aadhar Data Extraction Endpoint',status=200)
    elif(request.method == 'POST'):
        aadhar_card = request.FILES['aadhar']
        aadhar_data=aadhar_data_extractor(aadhar_card)
        return Response(aadhar_data,status=200)

@api_view(['POST','GET'])
def extract_pan_data(request):
    if(request.method == 'GET'):
        return Response('Pan Card Data Extraction Endpoint',status=200)
    elif(request.method == 'POST'):
        pan_card = request.FILES['pan']
        pan_type = request.data['type']
        pan_data = None
        if pan_type == 'old':
            pan_data=old_pan_data_extractor(pan_card)
        else:
            pan_data=new_pan_data_extractor(pan_card)
        
        return Response(pan_data,status=200)

@api_view(['POST','GET'])
def otp(request):
    if(request.method == 'GET'):
        return Response('OTP Generation Endpoint',status=200)
    elif(request.method == 'POST'):
        phone = request.data['phone']
        send_otp(phone)
        return Response({'message':'sent'},status=200)

@api_view(['POST','GET'])
def otp_verification(request):
    if(request.method == 'GET'):
        return Response('OTP Verification Endpoint',status=200)
    elif(request.method == 'POST'):
        phone = request.data['phone']
        otp = request.data['otp']
        return Response(verify_otp(phone,otp),status=200)

@api_view(['POST','GET'])
def signup(request):
    if(request.method == 'GET'):
        return Response('Signup Endpoint',status=200)
    elif(request.method == 'POST'):
        name=request.data['name']
        dob=request.data['dob']
        father=request.data['father']
        aadhar=request.data['aadhar']
        pan=request.data['pan']
        phone = request.data['phone']
        return Response(create_Account(name,dob,father,aadhar,pan,phone),status=200)

@api_view(['POST','GET'])
def login(request):
    if(request.method == 'GET'):
        return Response('Login Endpoint',status=200)
    elif(request.method == 'POST'):
        phone=request.data['phone']
        otp=request.data['otp']
        if(verify_otp(phone,otp)['message']=='Verified'):
            print(1)
            user_obj=get_Account_by_phone(phone)
            if(user_obj['found']):
                return Response({'message':'User Found','user':user_obj['user']},status=200)
            else:
                return Response({'message':'User Doesn\'t Exist'},status=200)
        else:
            return Response({'message':'Wrong OTP'},status=200)

@api_view(['POST','GET'])
def generate_qr(request):
    if(request.method == 'GET'):
        return Response('QR Code Generator Endpoint',status=200)
    elif(request.method == 'POST'):
        acc_id=request.data['acc_id']
        return Response({'qr_code':generate_qr_by_acc(acc_id)},status=200)

@api_view(['POST','GET'])
def send_money(request):
    if(request.method == 'GET'):
        return Response('Send Money Endpoint',status=200)
    elif(request.method == 'POST'):
        sender=request.data['sender']
        reciever=request.data['reciever']
        amount=request.data['amount']
        otp=request.data['otp']
        phone=request.data['phone']
        if(verify_otp(phone,otp)['message']=='Verified'):
            if(create_transaction(sender,reciever,amount)):
                return Response({'message':'Verified'},status=200)
            else:
                return Response({'message':'Insufficient Funds'},status=400)
        else:
            return Response({'message':'Wrong OTP'},status=400)

@api_view(['GET'])
def get_transaction(request):
    if(request.method=='GET'):
        sender = request.query_params['acc_id']
        return Response(get_transactions(sender),status=200)


@api_view(['POST','GET'])
def admin_login(request):
    if(request.method == 'GET'):
        return Response('Admin Login Endpoint',status=200)
    elif(request.method == 'POST'):
        phone=request.data['phone']
        pas=request.data['password']
        return Response(get_admin(phone,pas))

