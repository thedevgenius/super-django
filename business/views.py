from django.shortcuts import render, redirect
from django.views import View
from .models import Business, Category
from django.shortcuts import get_object_or_404
# Create your views here.
class CategoryListView(View):
    def get(self, request):
        categories = Category.objects.filter(is_active=True, level=1)
        return render(request, 'business/category_list.html', {'categories': categories})


class BusinessListView(View):
    def get(self, request, slug):
        category = Category.objects.get(slug=slug, is_active=True)
        businesses = Business.objects.filter(status='published', is_active=True, category=category)
        return render(request, 'business/business_list.html', {'category': category, 'businesses': businesses})
    

class BusinessDetailView(View):
    def get(self, request, slug):
        business = get_object_or_404(Business, slug=slug)
        return render(request, 'business/business_detail.html', {'business': business})
    
class BusinessAddView(View):
    def get(self, request):
        categories = Category.objects.filter(is_active=True, level=1)
        return render(request, 'business/business_add.html', {'categories': categories})
    
    def post(self, request):
        # Handle form submission logic here
        name = request.POST.get('business_name')
        category_id = request.POST.get('category')
        category = get_object_or_404(Category, id=category_id, is_active=True)

        Business.objects.create(
            owner=request.user,
            name=name,
            category=category,
            status='draft',
            is_active=False
        )
        return redirect('home')  # Redirect to the business detail page after creation
        