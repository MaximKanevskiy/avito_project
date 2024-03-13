from django.urls import path, re_path
from .views import SearchView, GetAllCategoriesView, PageNotFoundView, SetCategoryID, SetLocationID

urlpatterns = [
    path('', GetAllCategoriesView.as_view(), name='get_all'),
    path('search/', SearchView.as_view(), name='search'),
    path('set-category/', SetCategoryID.as_view(), name='set_category'),
    path('set-location/', SetLocationID.as_view(), name='set_location'),
    re_path(r'^.*$', PageNotFoundView.as_view(), name='page_not_found')
]
