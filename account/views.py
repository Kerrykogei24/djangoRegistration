
from django.shortcuts import redirect, render
from .forms import UserRegistrationForm
import random
from django.contrib.auth.models import User
from .email import send_otp
from django.contrib.auth.hashers import make_password
from .models import Profile
from django.contrib import messages

from django.http import HttpResponse
from django.contrib.auth import authenticate,login



def index(request):
 
    return render(request,'index.html')


def register(request):
    if request.method == 'POST':
        reg_form = UserRegistrationForm(request.POST)
     
        if reg_form.is_valid():
            email = reg_form.cleaned_data['email']
            username = reg_form.cleaned_data['username']
            password1 = reg_form.cleaned_data['password1']

            request.session['email']= email
            request.session['username'] = username
            request.session['password'] = password1
          

            otp = random.randint(1000,9999)
            request.session['otp'] = otp
            print('YOUR OTP IS' ,otp)
          
            # message = f'Your OTP is {otp}'

            # send_otp(email,message)
            return redirect ('/registration/otp')

    else:
        reg_form = UserRegistrationForm()
      

    context ={'regForm':reg_form}
    return render (request, 'register.html', context)



def otpVerification(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        otp =request.session.get('otp')
        user = request.session['username']
        hash_pwd = make_password(request.session.get('password'))
        email_address = request.session.get('email') 

        if int(otp)== otp:
            User.objects.create(username = user, email=email_address,password=hash_pwd)

            request.session.delete('otp')
            request.session.delete('user')
            request.session.delete('email')
            request.session.delete('password')
        

            messages.success(request,'Registration Successfully Done !!')
            return redirect('/login/')
        else:
            messages.error(request, 'Inncorect OTP')

    return render(request,'registration-otp.html')


def userLogin(request):

    try :
        if request.session.get('failed') > 2:
            return HttpResponse('<h1> You have to wait for 5 minutes to login again</h1>')
    except:
        request.session['failed'] = 0
        request.session.set_expiry(100)



    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
     
        user = authenticate(request,username=username,password=password)
        if user is not None:
            request.session['username'] = username
            request.session['password'] = password
            otp = random.randint(1000,9999)
            request.session['login_otp'] = otp
            print('YOUR OTP IS' ,otp)
            # message = f'your otp is {otp}'
            # send_otp(email,message)
            return redirect('/login/otp/')
        else:
            messages.error(request,'username or password is wrong')
    return render(request,'login.html')




def otpLogin(request):
    if request.method == "POST":
        username = request.session['username']
        password = request.session['password']
        otp = request.session.get('login_otp')
        u_otp = request.POST['otp']
        if int(u_otp) == otp:
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                request.session.delete('login_otp')
                messages.success(request,'login successfully')
                return redirect('/')
        else:
            messages.error(request,'Wrong OTP')
    return render(request,'login-otp.html')
