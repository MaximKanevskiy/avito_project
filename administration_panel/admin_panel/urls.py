from django.urls import path
from .views import GetAllCategoriesView

urlpatterns = [
    path('', GetAllCategoriesView.as_view(), name='get_all'),
]
