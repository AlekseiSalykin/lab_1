from bs4 import BeautifulSoup  # импортируем библиотеку BeautifulSoup
import requests  # импортируем библиотеку requests
from openpyxl import load_workbook

def parse():
    url = 'https://snovonovo.com/product-category/apple-iphone/page/2/'  # передаем необходимы URL адрес
    page = requests.get(url)  # отправляем запрос методом Get на данный адрес и получаем ответ в переменную
    src = page.text
    print(page.status_code)  # смотрим ответ
    soup = BeautifulSoup(src, "html.parser")  # передаем страницу в bs4

    block_title = soup.findAll(class_='text-clamp text-clamp-2 head-product')
    block_price = soup.findAll('div', class_='price_for_grid redbrightcolor floatleft rehub-btn-font mr10')# находим  контейнер с нужным классом

    price_list_for_calculations = []
    price_list = []
    iphone_name = []

    for data_title in block_title:
        iphone_name.append(data_title.text.strip())

    for data_price in block_price:
        if data_price.find('bdi'):
            price_list_for_calculations.append(data_price.text.strip().replace('₽', '').replace(' ', ''))
            price_list.append(data_price.text.strip())

    iphone_dict = dict(zip(iphone_name, price_list))

    price_list_for_calculations = [int(i) for i in price_list_for_calculations]
    summ = sum(price_list_for_calculations)
    minimum = min(price_list_for_calculations)
    maximum = max(price_list_for_calculations)

    wb = load_workbook('таблица.xlsx')
    ws = wb['price']
    for i in iphone_dict.items():
        ws.append(i)
    wb.save('таблица.xlsx')
    wb.close()

    print("Минимальная цена: ", minimum)
    print("Максимальная цена: ", maximum)
    print("Среднее: ", summ / len(price_list_for_calculations))
    print(iphone_dict)


