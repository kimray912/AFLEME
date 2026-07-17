from .models import Category

def categories_list(request):
    return {'global_categories': Category.objects.all()}