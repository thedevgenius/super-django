
from django.urls import path
from .views import HomePage, BlankPage, LocationPage

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('blank/', BlankPage.as_view(), name='blank'),
    path('location/', LocationPage.as_view(), name='location'),
]
