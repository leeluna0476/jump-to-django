from django.urls import path

from . import views

app_name = 'common'

urlpatterns = [
        path('github/oauth/', views.github_oauth, name='github_oauth'),
        path('github/callback/', views.github_callback, name='github_callback'),
        path('logout/', views.logout_view, name='logout'),
]
