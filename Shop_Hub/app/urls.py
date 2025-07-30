from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path('',views.index_view,name='index'),
    path('estate/<int:category_id>/',views.estate_detail_views, name = 'estate_detail'),
    path('feedback_response',views.user_estate_feedback_view,name='feedback_response'),

    path('estate_like/<int:estate_id>/',views.user_estate_like_view,name = 'estate_like'),
    path('favorite_list',views.favorite_like_view, name = 'favorite_list'),


    path('about',views.about_view,name='about')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
