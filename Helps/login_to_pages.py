import requests
'''
Данная функция получает на вход почту и пароль от аккаунта memorycode, получает access_token для данного аккаунта
а затем выдает все созданные страницы пользователя словарем в формате: {'page_name': 'page_id','page_name1': 'page_id1'}

Converts email and password to user's pages with id's
'''

def get_pages_from_email(login,password): #login - почта     password - пароль от аккаунта

    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    }
# 
    params = {
    "email": login,                 # параметры для запроса токена
    "password": password,
    "device": "bot-v0.0.1"
    }

    response = requests.post(
    'https://mc.dev.rand.agency/api/v1/get-access-token',               # получение токена 
    headers=headers,params=params
    )
    token = response.json()['access_token']     # отделение токена в стринговом формате

    headers['Authorization'] = str('Bearer ' + token)   # добавление полученного токена в headers


    getter = requests.get(
        'https://mc.dev.rand.agency/api/cabinet/individual-pages',          # получение страниц пользователя по его токену
        headers=headers
    )
    get = getter.json()

    result = {}     

    for field in get:
        name = field['name']       # парсинг полученной страницы
        page_id = field['link'][-8:]                                      #Парсятся поля name и link, для получения названия страницы и id (link - формате ссылке, где последние 8 символов - id)
        result[name] = page_id

    return result, token



if __name__ == '__main__':
    email = 'team63@hackathon.ru'
    password = 'wHe7fVE7'
    pages = get_pages_from_email(login=email,password=password)
    print(pages)

 