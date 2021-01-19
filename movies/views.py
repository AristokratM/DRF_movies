from django.http import HttpResponse
from .models import Category


def index(request):
    categories = Category.objects.all()
    return HttpResponse(f'<h1>{categories}</h1>')
