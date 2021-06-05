from django.shortcuts import render

from erp.models import Category

def category_list(request):
    data = {
        'title' : 'Listado de Categorias',
        'categories' : Category.objects.all()
    }
    return render(request, 'category/list.html', data)