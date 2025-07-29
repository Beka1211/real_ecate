from django.shortcuts import render, get_object_or_404, redirect
from pyexpat.errors import messages

from .models import Estate,Category,Favorite

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

def user_estate_like_view(request, estate_id):
    if request.method == 'POST':
        estate = get_object_or_404(Estate, id=estate_id)

        like_exits = Favorite.objects.filter(user=request.user, estate=estate).exists().first()
        if not like_exits:
            like = Favorite(user=request.user, estate=estate)
            like.save()
        else:
            like_exits.delete()
        return redirect('index')
    return redirect('index')

def favorite_like_view(request):
    if not request.user.is_authenticated:
        messages.error(request,messages='Войдите в систему')
        return redirect('index')
    else:

        return render(request, 'main/favorite_list.html')
