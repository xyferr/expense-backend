from django.shortcuts import redirect, render
from django.views import View
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage

from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator

# Create your views here.
class EmailValidationView(View):
    def post(self,request):
        data=json.loads(request.body)
        email=data['email']
        
        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid'},status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'Sorry, this email is already taken'},status=409)
        
        return JsonResponse({'email_valid':True})
        

class UsernameValidationView(View):
    
    def post(self,request):
        data=json.loads(request.body)
        username=data['username']
        
        if not str(username).isalnum():
            return JsonResponse({'username_error':'Username should only contain alphanumeric characters'},status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'Sorry, this username is already taken'},status=409)
        
        
        return JsonResponse({'username_valid':True})
    
    
    
class RegistrationView(View):
    
    def get(self,request):
        return render(request,'authentication/register.html')
    
    def post(self,request):
        #Get user data
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        
        context ={
            'fieldValues':request.POST
        }
        
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)<6:
                    messages.error(request,'Password too short')
                    return render(request,'authentication/register.html',context)
                
                user = User.objects.create_user(username=username,email=email)
                user.set_password(password)
                user.is_active=False
                # user.save()
                print("User created")
                messages.success(request,'User created successfully')
                try:
                    #path to the view
                    #uid64=force_bytes(urlsafe_base64_encode(user.pk))
                    domain = get_current_site(request).domain
                    link = reverse('activate',kwargs={
                        'uidb64':urlsafe_base64_encode(force_bytes(user.pk)),
                        'token':token_generator.make_token(user)
                    })
                    activate_url = 'http://'+domain+link
                    
                    
                    email_subject = f"Hi {user.username}, Activate your account"
                    email_body = 'Hi '+user.username+' Click the link below to activate your account\n'+activate_url
                    email = EmailMessage(
                        email_subject,
                        email_body,
                        "ROHIT <star080war@gmail.com>",
                        [user.email],
                    )
                    email.send(fail_silently=False)
                    messages.success(request,'Email sent successfully')
                
                except Exception as e:
                    messages.warning(request,'Unable to send email')
                    print(e)
        return render(request,'authentication/register.html')
    
class VerificationView(View):
    def get(self,request,uidb64,token):
        return redirect('login')
    
