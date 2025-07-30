from django.shortcuts import render, get_object_or_404, redirect
from pyexpat.errors import messages

from user.models import MyUser
from .models import Estate, Category, Favorite, Feedback, FeedbackResponse


def index_view(request):
    parent_categories=Category.objects.filter(parent_category__isnull=True)
    return render(request, 'main/index.html', {'parent_categories':parent_categories})

def estate_detail_views(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    child_categories = Category.objects.filter(parent_category=category)

    recommends_estate = Estate.objects.filter(category__in=child_categories).exclude(
        id__in=child_categories.values_list('id', flat=True))
    estates_like_quantity = Estate.objects.filter(category__in=child_categories).count()
    if child_categories.exists():
        return render(request, template_name='main/child.html', context={
            'category':category,
            'child':child_categories,
            'recommends_estate':recommends_estate,
            'estates_like_quantity': estates_like_quantity,
        })

    else:
        estates = Estate.objects.filter(category=category, is_active=True)
        return render(request, template_name='main/estate_detail.html', context={
            'category': category,
            'estates': estates
        })


def user_estate_feedback_view(request):
    estate = get_object_or_404(Estate)

    if request.method == 'POST':
        comment = request.POST['comment']
        Feedback.objects.create(
            user=MyUser,
            estate=estate,
            comment=comment,
        )
        messages.success(request, 'комментарий добавлен')
        return redirect('user_estate_feedback')

    feedbacks = estate.feedback_set.all().order_by('-created_at')
    return render(request, 'main/feedback.html', {
        'estate': estate,
        'feedbacks': feedbacks,
    })


def user_feedback_response_user(request, estate_id):
    feedback = get_object_or_404(Feedback, id=estate_id)

    if request.method == 'POST':
        comment = request.POST['comment']

        FeedbackResponse.objects.create(
            user=MyUser,
            feedback=feedback,
            comment=comment,
        )
        messages.success(request, "коментарий добавлен")
    return render(request,'main/feedback_response.html')


def user_estate_like_view(request, estate_id):
    if request.method == 'POST':
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