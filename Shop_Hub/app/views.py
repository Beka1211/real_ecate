from django.shortcuts import render, get_object_or_404
from .models import Estate,Category

def index_view(request):
    parent_categories=Category.objects.filter(parent_category__isnull=True)
    return render(request, 'main/index.html', {'parent_categories':parent_categories})

def estate_detail_views(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    child_categories = Category.objects.filter(parent_category=category)

    if child_categories.exists():
        return render(request, template_name='main/child.html', context={
            'category':category,
            'child':child_categories,
        })

    else:
        estates = Estate.objects.filter(category=category, is_active=True)
        return render(request, template_name='main/estate_detail.html', context={
            'category': category,
            'estates': estates
        })
