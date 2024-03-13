from django.http import JsonResponse, HttpResponseNotFound
from django.views import View
from anytree import search
from .locations import get_locations_tree
from .categories import get_all_categories_tree


categories_tree = get_all_categories_tree()


class GetAllCategoriesView(View):
    def get(self, request, *args, **kwargs):
        """Возвращает JsonResponse с данными всего дерева категорий при загрузке страницы"""
        response = JsonResponse(categories_tree, safe=False)
        response['Content-Type'] = 'application/json; charset=utf-8'
        return response


locations_tree = get_locations_tree()


class SearchView(View):
    def get(self, request):
        query = request.GET.get('query', '')
        result = search.findall(locations_tree, filter_=lambda node: query in node.name)
        return JsonResponse({'result': [node.name for node in result]})


class PageNotFoundView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound("Упс, страница не найдена")

# МЕНЯТЬ БАЗУ ДАННЫХ И СОХРАНЯТЬ СТАРУЮ БД
