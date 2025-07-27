from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path('',views.index_view,name='index'),
    path('estate/<int:category_id>/',views.estate_detail_views, name = 'estate_detail'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
