from django.http import JsonResponse
from django.views import View

raw_categories = {
    "Бытовая электроника": ["Товары для компьютера", "Фототехника", "Телефоны", "Планшеты и электронные книги",
                            "Оргтехника и расходники", "Ноутбуки", "Настольные компьютеры",
                            "Игры, приставки и программы", "Аудио и видео"],
    "Готовый бизнес и оборудование": ["Готовый бизнес", "Оборудование для бизнеса"],
    "Для дома и дачи": ["Мебель и интерьер", "Ремонт и строительство", "Продукты питания", "Растения",
                        "Бытовая техника", "Посуда и товары для кухни"],
    "Животные": ["Другие животные", "Товары для животных", "Птицы", "Аквариум", "Кошки", "Собаки"],
    "Личные вещи": ["Детская одежда и обувь", "Одежда, обувь, аксессуары", "Товары для детей и игрушки",
                    "Часы и украшения", "Красота и здоровье"],
    "Недвижимость": ["Недвижимость за рубежом", "Квартиры", "Коммерческая недвижимость", "Гаражи и машиноместа",
                     "Земельные участки", "Дома, дачи, коттеджи", "Комнаты"],
    "Работа": ["Резюме", "Вакансии"],
    "Транспорт": ["Автомобили", "Запчасти и аксессуары", "Грузовики и спецтехника", "Водный транспорт",
                  "Мотоциклы и мототехника"],
    "Услуги": ["Предложения услуг"],
    "Хобби и отдых": ["Охота и рыбалка", "Спорт и отдых", "Коллекционирование", "Книги и журналы", "Велосипеды",
                      "Музыкальные инструменты", "Билеты и путешествия"]
}


class CategoryNode:
    category_id = 0

    def __init__(self, name):
        CategoryNode.category_id += 1
        self.id = CategoryNode.category_id
        self.name = name
        self.children = []

    def add_child(self, child):
        """Добавляет дочерний узел в список детей текущего узла"""
        self.children.append(child)

    def to_dict(self):
        """Возвращает словарь, представляющий узел и его детей"""
        return {
            'id': self.id,
            'name': self.name,
            'children': [child.to_dict() for child in self.children]
        }


def get_all_categories_tree() -> CategoryNode:
    """Возвращает корневой узел древа категорий"""
    root_node = CategoryNode("ROOT")
    for category, sub_categories in raw_categories.items():
        category_node = CategoryNode(category)
        for sub_category in sub_categories:
            sub_category_node = CategoryNode(sub_category)
            category_node.add_child(sub_category_node)
        root_node.add_child(category_node)
    return root_node


def get_node_children(identifier: int) -> list:
    """Ищет дочерние узлы выбранного родительского узла"""
    full_catalogue = get_all_categories_tree()
    for node in full_catalogue.children:
        if node.id == identifier:
            return [child.to_dict() for child in node.children]


class GetCategoriesChildrenView(View):
    def get(self, request, *args, **kwargs) -> JsonResponse:
        """Возвращает JsonResponse с именами детей узла, идентификатор которого передан в запросе"""
        identifier = request.GET.get('id', None)
        if identifier is not None:
            identifier = int(identifier)
            children = get_node_children(identifier)
            if children:
                return JsonResponse([child.name for child in children], safe=False)
        return JsonResponse([])
