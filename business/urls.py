
from django.urls import path
from .views import BusinessDetailView, CategoryListView, BusinessListView, BusinessAddView

urlpatterns = [
    path('all-categories/', CategoryListView.as_view(), name='category_list'),
    path('<str:slug>/', BusinessDetailView.as_view(), name='business_details'),
    path('categoty/<str:slug>/', BusinessListView.as_view(), name='business_list'),
    path('business/add/', BusinessAddView.as_view(), name='business_add'),
]
