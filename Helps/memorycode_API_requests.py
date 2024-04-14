import requests
import fake_useragent
import random
import string
import pprint
import base64
def generate_random_letters():
    letters = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    return letters

api = 'https://memorycode.ru/api/'
# email = 'Alexikum@bk.ru'
# phone = '+79999023738'
# password = 'hL3GuNKG'

user = fake_useragent.UserAgent().random
session = requests.session()

endpoints = {
    # 'login_dev' : f'http://memorycode/api/v1/login?email={email}&phone={phone}&password={password}',
    'auth' : f'{api}login',
    # 'search' : f'',
    # 'Store ' : f'',
    # 'Get page' : f'',
    'contact' : f'{api}contact', #post
    'order' : f'{api}send-o rder', #post
    'tree' : f'https://familytree.memorycode.ru/api/tree', 
    'leaves' : f'https://familytree.memorycode.ru/api/tree/leaves', 
    'register' : f'{api}register', #post
    'reset_password' : f'{api}password/email' #post
}


def register(name, email, phone):

    password = generate_random_letters()

    json_data = {
        'name': name,
        'password': password,
        'email': email,
        'phone': phone,
        'password_confirmation': password,
        'checked': True,
        'sendPassword': True,
    }

    requests.post(endpoints['register'], json=json_data)
    

def auth(login, password):
    session = requests.session()

    json_data = {
    'password': password,
    'login': login,
    }

    response = session.post('https://memorycode.ru/api/login',json=json_data)

    return session, response.json()['user']['name']



def img_upload():
    url = "https://mc.dev.rand.agency/api/media/upload/94157953"

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "ru,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "multipart/form-data"
    }

    # Предположим, у вас есть файл, который вы хотите загрузить
    files = {'file': open('photos/925776934_photo.jpg', 'rb')}


    response = requests.post(url, headers=headers, params=files, verify=False)
    
    with open('photo.txt', 'w', encoding='utf-8') as file:
        file.write(response.text)
    
    return response.text

# print(img_upload())

def put(id, token):
# 1410|F9KvyyJcOUzqLa3TuWmiTnXiLUJEtUWB8DBJHhq4
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}',

    }

    params = {
        'name': "Tim",
        'page_type_id': "1",
        'epitaph': 'Gay ass nigga ahh goofy nigga ypu gay',
        "start": {
            "day": "02",
            "month": "01",
            "year": "2006"
        },
        "end": {
            "day": "03",
            "month": "01",
            "year": "2024"
        }
    }

    # 94157953
    url = f'https://mc.dev.rand.agency/api/page/{id}'
    response = requests.put(url, headers=headers, json=params).json()

    return response

# print(put(id=94157953, token='1410|F9KvyyJcOUzqLa3TuWmiTnXiLUJEtUWB8DBJHhq4'))



def put(data: dict):  # data is a dictionary
    id = data['page_id_5']
    file_name = data['photo']
    with open(file_name, 'rb') as f:
        image_data = f.read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        'Authorization': f"Bearer {data['token']}"
    }
    params = {
        'name': data['name'],
        'page_type_id': "1",
        'epitaph': data['epitath'],
        "start": {
            "day": data['birth'][0] + data['birth'][1],
            "month": data['birth'][3] + data['birth'][4],
            "year": data['birth'][6] + data['birth'][7] + data['birth'][8] + data['birth'][9]
        },
        "end": {
            "day": data['death'][0] + data['birth'][1],
            "month": data['death'][3] + data['death'][4],
            "year": data['death'][6] + data['death'][7] + data['death'][8] + data['death'][9]
        },
        "main_image": f'data:image/jpg;base64,{image_base64}',
        "author_epitaph": data['auth_epi'],
        
        "biographies": [
        {
            "title": data['name'],
            "description": data['bio'],
            "page_id": id,
            "order": 1,
            "checked": 'true',

        }
    ],
        "page_information" : [
            {
                "page_id": id,
                "title": "Место рождения",
                "description": data['birthpalce'],
            },
            {
                "page_id": id,
                "title": "Место смерти",
                "description": data['deathplace'],
            }

        ]
    

    }

    i = data['page_id']
    url = f'https://mc.dev.rand.agency/api/page/{i}'

    res = requests.put(url, headers=headers, json=params)
    if res.status_code == 200:
        print('Success!')
    else: 
        print('Error...')



def main(data):
    put(data)

if __name__ == '__main__':
    data={
        'access_token': 'Bearer 2634|XwieHHDpMHkOkzmyihUlwwzU5hjja2iRtwYZUPz9',
        'page_id':'8860',
        'link_id':'94157953',
        'name':'Морозов Тимофей Дмитриевич',
        'start':'01.02.1978',
        'end':'01.10.2021',
        'author_epitaph':'YandexGPT',
        'epitaph':'Умер и умер',
        'bio':'TO BE DONE',
        "birth_place" : 'Москва, Тверская ул. 1',
        "death_place" : 'Санкт-Петербург, Невский 14',
        "image_name" : 'images.jpg',
        
          
    }
    main(data)

