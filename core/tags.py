from django import template
from django.db.models import Count
from .models import Category

register = template.Library()

@register.simple_tag()
def list_categories():
    categories = Category.objects.annotate(test_count=Count('test'))
    return categories