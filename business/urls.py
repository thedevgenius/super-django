
from django.urls import path
from .views import BusinessDetailView, CategoryListView

urlpatterns = [
    path('business-details/', BusinessDetailView.as_view(), name='business_details'),
    path('all-categories/', CategoryListView.as_view(), name='category_list'),
]
