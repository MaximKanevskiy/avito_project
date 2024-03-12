from django.urls import path
from django.views.generic import TemplateView
from .views import GetCategoriesChildrenView

urlpatterns = [
    path('get-categories-children', GetCategoriesChildrenView.as_view()),
    path('', TemplateView.as_view(template_name="admin_panel/index.html")),
]
