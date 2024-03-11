from django.urls import path
from .views import get_categories_children

urlpatterns = [
    path('', get_categories_children, name='get_categories_children'),
]
