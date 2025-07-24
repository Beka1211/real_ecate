from django.contrib import admin
from .models import Category, Estate, City, District, Image


class EstateAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'city', 'district', 'price', 'is_active')
    list_filter = ('category', 'city', 'district', 'is_active')
    search_fields = ('title', 'description')


admin.site.register(Category)
admin.site.register(Estate, EstateAdmin)
admin.site.register(City)
admin.site.register(District)
admin.site.register(Image)