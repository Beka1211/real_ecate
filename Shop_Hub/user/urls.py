from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path('register',views.user_register_view, name='register'),
    path('login',views.user_login_view, name='login'),
    path('logout',views.user_logout_view,name='logout'),
    path('profile_settings',views.user_profile_settings_view,name = 'profile_settings')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)