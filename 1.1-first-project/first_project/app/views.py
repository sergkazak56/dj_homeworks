from django.http import HttpResponse
from django.shortcuts import render, reverse
import datetime
import os


def home_view(request):
    template_name = 'app/home.html'
    # впишите правильные адреса страниц, используя
    # функцию `reverse`
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('current_time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }
    
    # context и параметры render менять не нужно
    # подбробнее о них мы поговорим на следующих лекциях
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    # обратите внимание – здесь HTML шаблона нет, 
    # возвращается просто текст
    # now = datetime.datetime.now()
    return render(request, 'app/current_time.html', {'now': datetime.datetime.now().strftime("%d %B %Y time: %H:%M:%S")})


def workdir_view(request):
    # по аналогии с `time_view`, напишите код,
    # который возвращает список файлов в рабочей 
    # директории
    dir_path = os.path.abspath(os.getcwd())
    dir_list = []
    file_list = []
    for item in os.listdir(os.getcwd()):
        if os.path.isdir(f"{dir_path}\{item}"):
            dir_list.append(f"{item} - директория")
        else:
            file_list.append(f"{item} - файл")
    return render(request, 'app/workdir.html', {'dir_path': dir_path, 'dir_list': sorted(dir_list) + sorted(file_list)})

