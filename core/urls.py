
from django.urls import path
from .views import HomePage, BlankPage

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('blank/', BlankPage.as_view(), name='blank'),
]
