from django.shortcuts import render
from .models import Estate

def index_view(request):
    return render(request, 'main/index.html')

def estate_detail_views(request, estate_id):
    estate = Estate.objects.get(id=estate_id)
    return render(request, 'main/estate_detail.html', {'estate': estate})