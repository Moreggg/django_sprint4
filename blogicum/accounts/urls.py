from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.CreateUser.as_view(), name='registration')
]
