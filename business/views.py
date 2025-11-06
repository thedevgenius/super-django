from django.shortcuts import render
from django.views import View
from .models import Business, Category

# Create your views here.
class CategoryListView(View):
    def get(self, request):
        categories = Category.objects.filter(is_active=True, level=0)
        return render(request, 'business/category_list.html', {'categories': categories})


class BusinessListView(View):
    def get(self, request):
        # businesses = Business.objects.filter(status='published', is_active=True)
        return render(request, 'business/business_list.html')
    

class BusinessDetailView(View):
    def get(self, request):
        # business = Business.objects.get(slug=slug, status='published', is_active=True)
        return render(request, 'business/business_detail.html')