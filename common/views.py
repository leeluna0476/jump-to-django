from django.shortcuts import render, redirect

# Create your views here.

from config import api_client
from django.http import JsonResponse
from . import urls
import requests

def github_oauth(request):
    client_id = api_client.CLIENT_ID
    redirect_uri = f'http://localhost:8000/{urls.app_name}/github/callback/'
    scope = 'read:user user:email'
    auth_url = (
        f"https://github.com/login/oauth/authorize?"
        f"client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
    )
    return redirect(auth_url)

def github_callback(request):
    code = request.GET.get('code')
    # invalid code
    if not code:
        return JsonResponse({'error': 'Authentication code is missing'} , status=400)

    # request access token
    token_url = 'https://github.com/login/oauth/access_token'
    client_id = api_client.CLIENT_ID
    client_secret = api_client.CLIENT_SECRET
    headers = {'Accept': 'application/json'}
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
    }

    response = requests.post(token_url, headers=headers, data=data)
    token_response = response.json()

    access_token = token_response.get('access_token')
    if not access_token:
        error_description = token_response.get('error_description', 'Unknown error')
        return JsonResponse({"error": f"Failed to get access token: {error_description}"}, status=400)


    # add user to my server

    return redirect('pybo:index')
