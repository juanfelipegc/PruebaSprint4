from django.shortcuts import render
from django.http import HttpResponse
import requests


def ping(request):
    return HttpResponse('True')


def getRole(request):
    user = request.user
    if user.is_authenticated:
        user = request.user
        auth0user = user.social_auth.get(provider="auth0")
        accessToken = auth0user.extra_data['access_token']
        url = "https://julypriets.auth0.com/userinfo"
        headers = {'authorization': 'Bearer ' + accessToken}
        resp = requests.get(url, headers=headers)
        userinfo = resp.json()
        role = userinfo['https://julypriets:auth0:com/role']
        return (role)
    else:
        return ""
