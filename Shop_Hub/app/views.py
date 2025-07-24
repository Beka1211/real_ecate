from django.shortcuts import render

def index_view(request):
    return render(request, 'main/index.html')

def estate_detail_views(request):
    return render(request, 'main/detail_estate')