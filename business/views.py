from django.shortcuts import render
from django.views import View
from .models import Business

# Create your views here.
class BusinessListView(View):
    def get(self, request):
        # businesses = Business.objects.filter(status='published', is_active=True)
        return render(request, 'business/business_list.html')