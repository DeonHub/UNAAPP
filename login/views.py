from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.urls import reverse

import requests
import json
import io
import os

from pay.models import MemberBusiness
from .models import *
# from superuser.models import AssignPaymentDuration, MakePayment
import datetime
from itertools import chain
from django.http import HttpResponse, HttpRequest 

import os
import environ

env = environ.Env()
environ.Env.read_env()


# fee_url = "https://cash.akwaabasoftware.com/api"
super_url = "https://super.akwaabasoftware.com/api"

# fee_url = "http://127.0.0.1:8000/api"
# super_url = "http://127.0.0.1:7000/api"


# def validate_fee_code(code):
    
#     validate_url = f"{fee_url}/validate-code/{code}/"

#     headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}
#     valid = requests.request("GET", validate_url, headers=headers).json()['success']

#     if valid == "True":
#         return True
#     else:    
#         return False



def validate_super_code(code):
    
    validate_url = f"{super_url}/validate-code/{code}/"

    headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}
    valid = requests.request("GET", validate_url, headers=headers).json()['success']

    if valid == "True":
        return True
    else:    
        return False




def login(request):

    template_name = 'login/login.html'

    if request.method == "POST":
        code = request.POST.get('code')

        valid_super = validate_super_code(code)


        if valid_super == True:
            messages.success(request, 'Login Successful') 
            return redirect('pay:index', code) 

        else:

            messages.error(request, 'Invalid code. Please contact Admin') 
            return HttpResponseRedirect(reverse('login:login')) 

                    
    else:               
        return render(request,  template_name)





# def index(request):
#     # if ClientDetails.objects.count() == 0 or  MemberDetails.objects.count()  == 0 :

#         template_name = 'login/index.html'
#         today = datetime.date.today()
        
#         if request.method == "POST":
#             code = request.POST.get('code')

#             # items = []
#             url = f"{fee_url}/assigned-fees/{code}/"
#             headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}
#             response = requests.request("GET", url, headers=headers).json()['success']
#             # print(response)


#             if response == False:  
#                 messages.error(request, 'Invalid code. Please contact Admin') 
#                 return HttpResponseRedirect(reverse('login:login'))     
#             else:
#                 info = json.dumps({"code": code})
#                 # CM.setcookie(request=request, cookie_name=LOGIN_COOKIE_NAME, cookie_value=info)

#                 messages.success(request, 'Login Successful') 
#                 return redirect('pay:index', code) 

                        
#         else:               
#             return render(request,  template_name)


def index(request):
    template_name = 'login/index.html'

    return render(request, template_name, {

    })



def reset(request):
    template_name = 'login/reset.html'

    if request.method == "POST":
        email = request.POST.get('email')


        payload = json.dumps({
            "email": email, 
        })


        url = f"{super_url}/reset-code/"


        headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}

        response = requests.request("POST", url, headers=headers, data=payload).json()
        # print(response)

        if response['success'] == True:
            member_id = response['member_id']
            usercode = response['usercode']

            businesses = MemberBusiness.objects.filter(member_id=member_id)

            for business in businesses:
                business.usercode = usercode
                business.save()


            messages.success(request, 'Access Code Reset Successful. Please check your email for your access code to login.') 
            return redirect('login:login') 

        else:
            messages.success(request, 'Access Code Reset Failed. Please check the email address provided.') 
            return redirect('login:reset') 

                                      
    else:               
        return render(request,  template_name)
 




def verification(request):
    template_name = 'login/verification.html'

    if request.method == "POST":
        code = request.POST.get('code')

        payload = json.dumps({
            "code": code, 
        })


        url = f"{super_url}/verify-user/"

        headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}

        response = requests.request("POST", url, headers=headers, data=payload).json()['success']
        # response = requests.request("POST", url, headers=headers, data=payload).json()
        # print(response)


        if response == True:

            messages.success(request, 'Verification Successful. Please check your email for your access code to login.') 
            return redirect('login:login') 

        else:
            messages.success(request, 'Verification Failed. Please check the email address provided.') 
            return redirect('login:verification') 


                                               
    else:               
        return render(request,  template_name)
 




def signup(request):
    template_name = 'login/signup.html'

    url = f"{super_url}/register-user/"
    
    headers = {'Content-Type': 'application/json', 'Cookie': 'csrftoken=4QyiPkebOBXrv202ShwWThaE1arBMWdnFnzdsgyMffO6wvun5PpU6RJBTLRIdYDo; sessionid=rsg9h5tu73jyo3hl2hvgfm0qcd7xmf92'}


    if request.method == 'POST':
        firstname = request.POST.get('firstname')

        surname = request.POST.get('surname')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        country = request.POST.get('country')

        try:
            image = request.FILES.get('image')
        except:
            image = None    


        medium = request.POST.get('medium')


        unaapp = UnaappUser.objects.create(
            name=firstname,
            email=email,
            image=image,
        )
        unaapp.save()



        payload={
            'firstname': firstname,
            'surname': surname,
            'email': email,
            'contact': contact,
            'medium': medium,
            'country': country
        }
        


        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload).json()['success']


        # print(response)

        if response == True:

            messages.success(request, 'Please check your email or SMS for verification code.') 
            return HttpResponseRedirect(reverse('login:verification'))  

        else:
            messages.success(request, 'User with email already exists.') 
            return HttpResponseRedirect(reverse('login:signup')) 
    else:
        return render(request, template_name, {

        })