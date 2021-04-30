import cv2
import numpy
import pytesseract
import re
from twilio.rest import Client
from api.models import Otp,Account,Transaction,Balance,Admin
from api.aadhar_utils import verify_aadhar
import qrcode
import base64
from io import BytesIO
import random
from operator import itemgetter
from fpdf import FPDF

def aadhar_data_extractor(aadhar_card):
    img = cv2.imdecode(numpy.fromstring(aadhar_card.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(img).split('\n')
    cleaned=[]
    for t in text:
        s = t.strip()
        s = t.replace('\n','')
        s = s.rstrip()
        s = s.lstrip()
        cleaned.append(s)
    
    cleaned = list(filter(None, cleaned))
    dob_index = None

    for i in range(len(cleaned)):
        temp = cleaned[i].lower()
        temp=temp.lower()
        if(':' in temp):
            if('dob' in temp or '008'):
                dob_index = i
    
    data = {}
    exceptions=[]
    try:
        data['name'] = cleaned[dob_index-1]
    except:
        data['name'] = ""
        exceptions.append('Name not Found')
    
    try:
        data['dob'] = cleaned[dob_index].split(':')[1].strip()
    except:
        data['dob'] = ""
        exceptions.append('DOB not Found')
    
    try:
        temp = cleaned[dob_index+1].lower()
        if('male' in temp):
            data['gender'] = "Male"
        else:
            data['gender'] = "Female"
    except:
        data['gender'] = ""
        exceptions.append('Gender not found')
    
    try:
        data['aadhar'] =  ''.join(filter(str.isdigit, cleaned[dob_index+2]))  
    except:
        data['aadhar'] = ""
        exceptions.append('Aadhar number not found')
    
    data['exceptions'] =exceptions


    return data

def old_pan_data_extractor(pan_card):
    img = cv2.imdecode(numpy.fromstring(pan_card.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(img).split('\n')
    cleaned=[]
    for t in text:
        s = t.strip()
        s = t.replace('\n','')
        s = s.rstrip()
        s = s.lstrip()
        if(len(s)>2):
            cleaned.append(s)

    cleaned = list(filter(None, cleaned))
    
    pan_index=None

    for i in range(len(cleaned)):
        temp = cleaned[i].lower()
        if('permanent' in temp) or ('account' in temp) or ('number' in temp):
            pan_index = i
    print(cleaned)
    data = {}
    exceptions=[]
    try:
        data['name'] = ''.join(i for i in cleaned[pan_index-3] if i.isalpha() and not i.islower() or i in ' ')
    except:
        data['name'] = ""
        exceptions.append('Name not Found')
    
    try:
        data['father_name'] = (''.join(i for i in cleaned[pan_index-2] if i.isalpha() and not i.islower() or i in ' ')).strip()
    except:
        data['father_name'] = ""
        exceptions.append('Father\'s Name not Found')
    
    try:
        data['dob'] = s = ''.join(i for i in cleaned[pan_index-1] if i.isdigit() or i in '-./\\') 
    except:
        data['dob'] = ""
        exceptions.append('DOB not Found')
    
    try:
        data['pan']=re.sub(r'\W+', '', cleaned[pan_index+1])
    except:
        data['pan'] = ""
        exceptions.append('Pan not found')
    
    
    data['exceptions'] =exceptions

    
    return data

def new_pan_data_extractor(pan_card):
    img = cv2.imdecode(numpy.fromstring(pan_card.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(img).split('\n')
    cleaned=[]
    for t in text:
        s = t.strip()
        s = t.replace('\n','')
        s = s.rstrip()
        s = s.lstrip()
        if(len(s)>2):
            cleaned.append(s)

    cleaned = list(filter(None, cleaned))
    name_index=None
    pan_index=None
    father_index=None
    dob_index=None
    
    for i in range(len(cleaned)):
        temp= cleaned[i].lower()
        if('permanent' in temp or 'account' in temp or 'number' in temp ):
            pan_index=i+1
        elif('name' in temp and 'father' not in temp):
            name_index=i+1
        elif('name' in temp and 'father' in temp):
            father_index=i+1
        elif('date' in temp):
            dob_index=i+1
    
    data = {}
    exceptions=[]
    try:
        data['name'] = ''.join(i for i in cleaned[name_index] if i.isalpha() and not i.islower() or i in ' ')
    except:
        data['name'] = ""
        exceptions.append('Name not Found')
    
    try:
        data['father_name'] = (''.join(i for i in cleaned[father_index] if i.isalpha() and not i.islower() or i in ' ')).strip()
    except:
        data['father_name'] = ""
        exceptions.append('Father\'s Name not Found')
    
    try:
        data['dob'] = s = ''.join(i for i in cleaned[dob_index] if i.isdigit() or i in '-./\\') 
    except:
        data['dob'] = ""
        exceptions.append('DOB not Found')
    
    try:
        data['pan']=re.sub(r'\W+', '', cleaned[pan_index])
    except:
        data['pan'] = ""
        exceptions.append('Pan not found')
    
    
    data['exceptions'] =exceptions

    return data

def send_otp(phone_num):
    account_sid = "ACf003389f0b50d6cdf499f5c35f4a6014"
    auth_token = "e4b4fd0eab827e14474cd305d454165c"
    client = Client(account_sid, auth_token)
    otp_gen=random.randint(000000,999999)
    message = client.messages \
                    .create(
                         body="Your OTP is " + str(otp_gen),
                         from_='+19257018143',
                         to='+91'+phone_num
                     )
    if(Otp.objects.filter(phone=phone_num)):
        Otp.objects.filter(phone=phone_num).update(otp=otp_gen)
    else:
        Otp.objects.create(otp=otp_gen,phone=phone_num)

def verify_otp(phone_num,otp_sent):
    print(phone_num,otp_sent)
    print(Otp.objects.filter(phone=phone_num,otp=otp_sent))
    if(Otp.objects.filter(phone=phone_num,otp=otp_sent)):
        return {'message':'Verified'}
    else:
        return {'message':'Not Verified'}

def create_Account(u_name,date,father_name,aadhar_num,pan_num,phone_num):
    if(Account.objects.filter(aadhar=aadhar_num)):
        return {'message':'User Exists'}
    else:
        Account.objects.create(name=u_name,dob=date,father=father_name,aadhar=aadhar_num,pan=pan_num,phone=phone_num)
        return {'message':'Signed Up'}

def get_Account_by_phone(phone_num):
    user=Account.objects.filter(phone=phone_num)
    if(user):
        return {'found':True,'user':user.values()[0]}
    else:
        return {'found':False}

def get_Accounts_by_status():
    users = Account.objects.filter(status=False).values()
    return users

def update_verification(user_obj):
    Account.objects.filter(acc_id=user_obj['acc_id']).update(status=True)

def scheduled_aadhar_verify():
    print('Verification Loop')
    users = get_Accounts_by_status()
    if(len(users)>0):
        for i in users:
            aadhar = i['aadhar']
            print('Verifying Aadhar '+aadhar)
            if(verify_aadhar(aadhar)):
                update_verification(i)
                print('Aadhar Verified')
            else:
                print('Could not verify!!')

def generate_qr_by_acc(acc_num):
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
    )
    qr.add_data(acc_num)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str

def create_transaction(s,r,amt):
    amt=float(amt)
    sender_balance=Balance.objects.filter(account_id=s).values()[0]['balance']
    reciever_balance=Balance.objects.filter(account_id=r).values()[0]['balance']
    if(sender_balance<amt):
        return False
    else:
        Transaction.objects.create(sender=Account.objects.get(acc_id=s),reciever=Account.objects.get(acc_id=r),amount=amt)
        sender_balance-=amt
        reciever_balance+=amt
        Balance.objects.filter(account_id=s).update(balance=sender_balance)
        Balance.objects.filter(account_id=r).update(balance=reciever_balance)
        return True

def get_transactions(s):
    debit=Transaction.objects.filter(sender=Account.objects.get(acc_id=s)).values()
    credit=Transaction.objects.filter(reciever=Account.objects.get(acc_id=s)).values()
    all_transactions=[]
    for i in debit:
        to_from_user_name=Account.objects.filter(acc_id=i['reciever_id']).values()[0]['name']
        temp=i
        temp['second_party']=to_from_user_name
        temp['time_stamp_formatted']=temp['time_stamp'].strftime('%Y-%m-%d %H:%M')
        all_transactions.append(temp)
    for i in credit:
        to_from_user_name=Account.objects.filter(acc_id=i['sender_id']).values()[0]['name']
        temp=i
        temp['second_party']=to_from_user_name
        temp['time_stamp_formatted']=temp['time_stamp'].strftime('%Y-%m-%d %H:%M')
        all_transactions.append(temp)
    all_transactions=sorted(all_transactions, key=itemgetter('time_stamp'),reverse = True)
    return all_transactions

def get_admin(phone_num,pas):
    user=Admin.objects.filter(phone=phone_num,password=pas)
    if(user):
        return {'message':'Admin Found','user':user.values()[0]}
    else:
        return {'message':'Admin Not Found','user':{}}
