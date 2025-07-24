from django.contrib import admin
from .models import Category,Estate,City,District

class EstateAdmin(admin.ModelAdmin):
    list_display = ('category','estate','city','district',)
    list_filter = ('district','city','category',)
admin.site.register(Category)
admin.site.register(Estate, EstateAdmin)
admin.site.register(City)
admin.site.register(District)