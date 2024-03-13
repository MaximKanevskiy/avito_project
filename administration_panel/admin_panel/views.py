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


def get_all_categories_tree() -> dict:
    """Возвращает данные всего дерева категорий"""
    root_node = CategoryNode("ROOT")
    for category, sub_categories in raw_categories.items():
        category_node = CategoryNode(category)
        for sub_category in sub_categories:
            sub_category_node = CategoryNode(sub_category)
            category_node.add_child(sub_category_node)
        root_node.add_child(category_node)
    return root_node.to_dict()


full_tree = get_all_categories_tree()


class GetAllCategoriesView(View):
    def get(self, request, *args, **kwargs):
        """Возвращает JsonResponse с данными всего дерева категорий при загрузке страницы"""
        response = JsonResponse(full_tree, safe=False)
        response['Content-Type'] = 'application/json; charset=utf-8'
        return response

# МЕНЯТЬ БАЗУ ДАННЫХ И СОХРАНЯТЬ СТАРУЮ БД
