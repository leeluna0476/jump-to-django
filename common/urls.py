from django.urls import path

from . import views

app_name = 'common'

urlpatterns = [
        path('login/', views.oauth_login, name='oauth_login'),
]
