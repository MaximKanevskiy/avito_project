from django.http import JsonResponse, HttpResponseNotFound
from django.views import View
from anytree import search

from .locations import get_locations_tree
from .categories import get_all_categories_tree


categories_tree = get_all_categories_tree()
locations_tree = get_locations_tree()


class GetAllCategoriesView(View):
    def get(self, request, *args, **kwargs):
        """Возвращает JsonResponse с данными всего дерева категорий при загрузке страницы"""
        response = JsonResponse(categories_tree, safe=False)
        response['Content-Type'] = 'application/json; charset=utf-8'
        return response


class SearchView(View):
    def get(self, request):
        query = request.GET.get('query', '')
        result = search.findall(locations_tree, filter_=lambda node: query in node.name)
        return JsonResponse({'result': [node.name for node in result]})


category_id = None
location_id = None


class SetIDView(View):
    global_id = None

    def post(self, request):
        global category_id, location_id
        id_str = request.POST.get('id', None)
        if id_str is not None:
            try:
                self.global_id = int(id_str)
                return JsonResponse({'status': 'success'}, status=200)
            except ValueError:
                return JsonResponse({'status': 'error', 'error': 'Invalid id'}, status=400)
        else:
            return JsonResponse({'status': 'error', 'error': 'No id provided'}, status=400)


class SetCategoryID(SetIDView):
    """Меняет глобальный идентификатор категории, соответственно значению, присланному по POST-запросу"""
    global_id = category_id


class SetLocationID(SetIDView):
    """Меняет глобальный идентификатор локации, соответственно значению, присланному по POST-запросу"""
    global_id = location_id


class PageNotFoundView(View):
    """Обрабатывает случай перехода по несуществующему пути"""
    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound("Упс, страница не найдена")

# МЕНЯТЬ БАЗУ ДАННЫХ И СОХРАНЯТЬ СТАРУЮ БД
