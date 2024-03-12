from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
        self.children.append(child)


def get_all_categories_tree():
    root_node = CategoryNode("ROOT")
    for category, sub_categories in raw_categories.items():
        category_node = CategoryNode(category)
        for sub_category in sub_categories:
            sub_category_node = CategoryNode(sub_category)
            category_node.add_child(sub_category_node)
        root_node.add_child(category_node)
    return root_node


def find_node(node, identifier):
    if node.id == identifier:
        return node
    for child in node.children:
        found_node = find_node(child, identifier)
        if found_node is not None:
            return found_node
    return None


def recursive_tree(full_tree, head_node_id):
    head_node = find_node(full_tree, head_node_id)
    if head_node is not None:
        return head_node.children
    return []


@csrf_exempt
def get_categories_children(request):
    if request.method == 'POST':
        full_tree = get_all_categories_tree()
        children_node_id = request.POST.get('microcategory_id')

        new_head = recursive_tree(full_tree, int(children_node_id) if children_node_id else 0)
        children = [child.name for child in new_head]
        return JsonResponse({'children': children})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
