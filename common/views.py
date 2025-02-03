from django.shortcuts import render, redirect

# Create your views here.
from config import api_client
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.views.decorators.http import require_POST, require_GET
from . import urls, models
import requests

# set credential scopes
# Authorization request -> to the resource owner
#def login(request):
#    if not request.user.is_authenticated: # or refresh token expired
#        return redirect('pybo:github_oauth')

@require_GET
def github_oauth(request):
    next_url = request.GET.get('next', 'pybo:index')

    client_id = api_client.CLIENT_ID
    redirect_uri = f'http://localhost:8000/{urls.app_name}/github/callback/?next={next_url}'
    scope = 'read:user user:email'
    auth_url = (
        f"https://github.com/login/oauth/authorize?"
        f"client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
    )
    return redirect(auth_url)

# after authorization being granted by the user
@require_GET
def github_callback(request):
    code = request.GET.get('code')
    # invalid code
    if not code:
        return JsonResponse({'error': 'Authentication code is missing'} , status=400)

    # request access token from the authentication server
    token_url = 'https://github.com/login/oauth/access_token'
    client_id = api_client.CLIENT_ID
    client_secret = api_client.CLIENT_SECRET
    headers = {'Accept': 'application/json'}
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
    }

    # check access token issuance
    response = requests.post(token_url, headers=headers, data=data)
    token_response = response.json()
    access_token = token_response.get('access_token')
    refresh_token = token_response.get('refresh_token')
    # if null == if the authentication server responds with an http 400 code with error parameters
    if not access_token:
        error_description = token_response.get('error_description', 'Unknown error')
        return JsonResponse({"error": f"Failed to get access token: {error_description}"}, status=400)

    # request protected resources from the resource server
    user_url = 'https://api.github.com/user'
    user_headers = {'Authorization': f'token {access_token}'}
    user_info = requests.get(user_url, headers=user_headers).json()

    username = user_info.get('login')

    # save the user object
    user = models.GithubUser.objects.get_or_create(username=username)[0]
    user.access_token = access_token
    user.refresh_token = refresh_token
    user.save()
    if not request.user.is_authenticated:
        login(request, user)

    next_url = request.GET.get('next', 'pybo:index')
    return redirect(next_url)

@require_POST
def logout_view(request):
    logout(request)
    next_url = request.POST.get('next', 'pybo:index')
    return redirect(next_url)
