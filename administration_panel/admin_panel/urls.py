from django.urls import path, re_path
from .views import SearchView, GetAllCategoriesView, PageNotFoundView

urlpatterns = [
    path('', GetAllCategoriesView.as_view(), name='get_all'),
    path('search/', SearchView.as_view(), name='search'),
    re_path(r'^.*$', PageNotFoundView.as_view(), name='page_not_found')
]
