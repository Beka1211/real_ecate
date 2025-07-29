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
    if not request.user.is_authenticated:
        return redirect('login')
    estate = get_object_or_404(Estate, id=estate_id)
    like_exits = Favorite.objects.filter(user=request.user, estate=estate).first()
    if like_exits:
        like_exits.delete()
    else:
        Favorite.objects.create(user=request.user, estate=estate)
    return redirect('index')

    #логика лайка

def favorite_like_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Войдите в систему')
        return redirect('index')

    favorites = Favorite.objects.filter(user=request.user)
    estates = [fav.estate for fav in favorites]

    return render(request, 'main/favorite_list.html', {'estates': estates})

    #страница где будут хранится все лайки у можно будет увиеть эти залайканные обявление\товары

def about_view(request):
    return render(request,'main/about.html')