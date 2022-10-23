from django.http import HttpResponse
from django.shortcuts import render, reverse

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }
def multiply(dict_: dict, value: float) ->dict:
    rezult = {}
    for key, val in dict_.items():
        rezult[key] = val * value
    return rezult

def recipes(request, dish):
    persons = request.GET.get('persons', '1')
    if persons.isdigit():
        persons = int(persons)
    else:
        persons = 1
    context = {}
    context['dish'] = dish
    context['persons'] = persons
    if dish in DATA:
        context['recipe'] = multiply(DATA[dish], persons)
    else:
        context['recipe'] = {}
    return render(request, 'calculator/index.html', context)

