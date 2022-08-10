from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
import json
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt #, csrf_protect, requires_csrf_token
from django.contrib.auth import authenticate, login, logout
from rest_framework_jwt.settings import api_settings
from .models import Url as UrlModel
import random

chars = 'abcdefghijklmnopqrstufwxyz'

# Create your views here.
@csrf_exempt
def logins(request):
    status = "ok"
    token = ''
    code = 200

    if request.method == "POST":
        try:
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(request.user)
            token = jwt_encode_handler(payload)
            body_request = request.body.decode('utf-8')
            body_request = json.loads(body_request)
            user = authenticate(request, username=body_request["username"], password=body_request["password"])
            login(request, user)
                
        except:
            status = 'failed'
            code = 400
            token = ''

        return JsonResponse(
            {
                'status': status,
                'token': token
            }, status = code
        )
    else:
        return JsonResponse(
            {
                'status': 'failed',
                'message': 'method invalid'
            }
        )     

@csrf_exempt
def register(request):
    status = "ok"
    message = "Akun berhasil dibuat!"
    code = 200
    
    if request.method == "POST":
        body_request = request.body.decode('utf-8')
        body_request = json.loads(body_request)

        try:
            first_name = body_request["fullname"].split(' ')[0]
            last_name = ' '.join(body_request["fullname"].split(' ')[1:])

            new_user = User.objects.create_user(
                username = body_request["username"],
                first_name = first_name,
                last_name = last_name,
                email = body_request["email"],
                password = body_request["password"]
            )
            new_user.save()

        except:
            status = "failed"
            message = "Akun gagal dibuat!"
            code = 400

        return JsonResponse(
            {
                "status": status,
                "message": message,
            }, status = code
        )
    else:
        return JsonResponse(
            {
                'status': 'failed',
                'message': 'method invalid'
            }
        )

@csrf_exempt
def shortUrl(request):
    status = 'ok'
    print(request.user.id)
    message = ''

    if request.method == "POST":
        try:
            body_request = json.loads(request.body.decode('utf-8'))
            url = body_request['url']
            random_string = f"http://{request.META['HTTP_HOST']}/"
            for i in range(10):
                random_string += chars[random.randint(0, len(chars)-1)]
            print(random_string)
            message = 'YOUR SHORT URL: '+ random_string
            
            if request.user.is_authenticated:
                user_id = request.user.id
                url_querySet = UrlModel.objects.create(
                    long_url = url,
                    short_url = random_string,
                    owner_id = user_id
                )

            else:
                url_querySet = UrlModel.objects.create(
                    long_url = url,
                    short_url = random_string,
                )

            url_querySet.save()
        
        except:
            status = 'failed'
            message = ''

        return JsonResponse(
            {
                'status': status,
                'message': message
            }
        )

    else:
        return JsonResponse(
            {
                'status': 'failed',
                'message': 'method invalid'
            }
        )

@csrf_exempt
def listUrl(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            url_list = UrlModel.objects.filter(owner_id=request.user.id)
        else:
            url_list = UrlModel.objects.filter(owner_id=0)

        results = []

        for i in url_list:
            results.append(i.as_dict())

        return JsonResponse(results, safe=False)
    else:
        return JsonResponse(
            {
                'status': 'failed',
                'message': 'method invalid'
            }
        )

@csrf_exempt
def editUrl(request, id_url):
    status = 'ok'
    message = ''
    if request.user.is_authenticated:
        if request.method == "PUT":
            try:
                get_url = UrlModel.objects.get(pk=id_url)
            except:
                get_url = None
                status = 'failed'

            if get_url:
                body_request = json.loads(request.body.decode('utf-8'))
                url = body_request['url']
                
                if f"https://{request.META['HTTP_HOST']}" in url:
                    pass
                elif f"http://{request.META['HTTP_HOST']}" in url:
                    pass
                else:
                    url = f"http://{request.META['HTTP_HOST']}/{url}"

                get_url.short_url = url
                get_url.save()

                message = f"YOUR SHORT CUSTOM URL: {url}"

            return JsonResponse(
                {
                    'status':status,
                    'message': message
                }
            )
    else:
        return JsonResponse(
            {
                'status': 'failed',
                'message': 'method invalid'
            }
        )

@csrf_exempt
def deleteUrl(request, id_url):
    if request.method == "DELETE":
        if request.user.is_authenticated:
            try:
                get_url = UrlModel.objects.filter(owner_id=request.user.id).get(pk=id_url)
            except:
                get_url = None
        else:
            try:
                get_url = UrlModel.objects.filter(owner_id=0).get(pk=id_url)
            except:
                get_url = None
            
        if get_url:
            get_url.delete()

            return JsonResponse(
                {
                    'status': 'ok',
                    'message': 'URL has been deleted!'
                }
            )
        
        else:
            return JsonResponse(
                {
                    'status': 'failed',
                    'message': 's'
                }
            )
    else:
        return JsonResponse(
            {
                'status': 'failed',
                'message': 'method invalid'
            }
        )

def openShortedUrl(request, url):

    url_querySet = UrlModel.objects.filter(short_url__contains = url)
    if len(url_querySet) != 0:
        url = url_querySet[0].as_dict()
        url = url['long_url']
        if 'http://' in url:
            pass
        else:
            url = 'http://' + url

        return HttpResponseRedirect(url)
        

def logout_view(request):
    logout(request)

    return JsonResponse({'message': 'success logout'})