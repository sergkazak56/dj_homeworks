import math
import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
import csv

def index(request):
    return redirect(reverse('bus_stations'))

def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    with open("data-398-2018-08-30.csv", newline='\n', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        csv_list = list(reader)
    # csv_list = get_stations()
    csv_list.sort(key=lambda x: x['District'])
    page_number = request.GET.get('page', '1')
    if page_number.isdigit():
        if int(page_number) < 1:
            page_number = 1
        elif int(page_number) > math.ceil(len(csv_list) / 10):
            page_number = math.ceil(len(csv_list) / 10)
        else:
            page_number = int(page_number)
    elif page_number == 'last':
        page_number = math.ceil(len(csv_list) / 10)
    else:
        page_number = 1
    paginator = Paginator(csv_list, 10)
    page = paginator.get_page(page_number)
    context = {
        'bus_stations': page
    }
    return render(request, 'stations/index.html', context)

# Получить актуальный листинг остановок напрямую с портала https://data.mos.ru
# можно через API для этого надо получить ключ и ввести его в
# переменную API_KEY. И в функции bus_stations вместо открытия и
# считывания файла "data-398-2018-08-30.csv" (строки 14-16 кода) следует
# csv_list присвоить значение get_stations() (строка 17 кода)
# Но это очень тормозит работу сервера, поэтому лучше обновлять данные в файле
# с определенной периодичностью.

API_KEY = '*************************************'

def get_stations():
    link = f'https://apidata.mos.ru/v1/datasets/752/count?api_key={API_KEY}'
    response_get = requests.get(link)
    count = int(response_get.text)
    if count >= 10000:
        link = f'https://apidata.mos.ru/v1/datasets/752/rows?$top=9999&api_key={API_KEY}'
    else:
        link = f'https://apidata.mos.ru/v1/datasets/752/rows?$top={count}&api_key={API_KEY}'
    response_post = requests.post(link)
    stations_list=[]
    for item in response_post.json():
        dict_ = {'Name': item['Cells']['StationName'], 'District': item['Cells']['District'], 'Street': item['Cells']['PlaceDescription']}
        stations_list.append(dict_)
    return stations_list