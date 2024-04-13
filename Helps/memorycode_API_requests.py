import requests
import fake_useragent
import random
import string

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



def reset_password(email):

    json_data = {
    'email': email,
    }

    requests.post(endpoints['reset_password'], json=json_data)


def contact(name, email, phone, category, question):

    json_data = {
        'name': name,
        'email': email,
        'phone': phone,
        'category': category,
        'question': question,
        }

    requests.post('https://memorycode.ru/api/contact', json=json_data)
    

def store():
    json_data = {
    'id': 90285,
    'name': 'Саша Пупкин',
    'surname': None,
    'patronym': None,
    'birthday_at': '2018-06-07 00:00:00',
    'died_at': '2024-05-04 00:00:00',
    'epitaph': 'Лол Кек Чебурек',
    'author_epitaph': "'XD",
    'video_links': None,
    'external_links': None,
    'published_page': True,
    'accessible_by_password': False,
    'access_password': None,
    'user_id': 51828,
    'master_id': None,
    'page_type_id': 2,
    'created_at': '2024-04-02T11:07:48.000000Z',
    'updated_at': '2024-04-05T23:07:52.000000Z',
    'deleted_at': None,
    'slug': 30421140,
    'burial_id': None,
    'price': None,
    'commission': None,
    'payment_id': None,
    'video_images': None,
    'blank_id': None,
    'is_blank': False,
    'is_vip': False,
    'views': 0,
    'visitors': 0,
    'lead_id': 37286161,
    'index_page': False,
    'filled_fields': [
        'epitaph',
        'main_image',
    ],
    'position': None,
    'is_referral': False,
    'banner_enabled': True,
    'locale': 'ru',
    'was_indexed': False,
    'qr_hidden': False,
    'historical_status_id': 1,
    'count_filled_fields': 2,
    'parent_tree_id': None,
    'custom_birthday_at': None,
    'custom_died_at': None,
    'pages': [],
    'photos': [],
    'audio_records': [],
    'video_records': [],
    'video_previews': [],
    'itemComments': [
        {
            'title': 'Опубликованные отзывы',
            'comments': [],
        },
        {
            'title': 'Новые внешние отзывы',
            'comments': [],
        },
    ],
    'main_image': 'https://src.memorycode.ru/storage/app/public/42900/1712056068.jpg',
    'start': {
        'day': '07',
        'month': '06',
        'year': 2018,
    },
    'end': {
        'day': '04',
        'month': '05',
        'year': 2024,
    },
    'lastName': None,
    'firstName': 'Саша Пупкин',
    'link': 'https://memorycode.ru/page/30421140',
    'free_access': True,
    'full_name': ' Саша Пупкин ',
    'burial_place': False,
    'page_type_name': 'pageType.short',
    'count_fields': 3,
    'burial': None,
    'media': [
        {
            'id': 42900,
            'model_type': 'App\\Models\\Page\\Page',
            'model_id': 90285,
            'uuid': 'c5a7834f-a211-442a-b780-3676d467dfa6',
            'collection_name': 'main_image',
            'name': 'media-libraryMqbvbx',
            'file_name': '1712056068.jpg',
            'mime_type': 'image/jpeg',
            'disk': 'public',
            'conversions_disk': 'public',
            'size': 19366,
            'manipulations': [],
            'custom_properties': [],
            'responsive_images': [],
            'order_column': 41105,
            'created_at': '2024-04-02T11:07:48.000000Z',
            'updated_at': '2024-04-02T11:07:48.000000Z',
        },
    ],
    'child_pages': [],
    'comments_public': [],
    'comments_not_public': [],
    'place': {
        'id': 3732,
        'cemetery_id': None,
        'details': None,
        'how_get': None,
        'latitude': None,
        'longitude': None,
        'page_id': 90285,
    },
    'biographies': [
        {
            'id': 16238,
            'title': None,
            'description': None,
            'page_id': 90285,
            'created_at': '2024-04-02T11:09:50.000000Z',
            'updated_at': '2024-04-02T11:09:50.000000Z',
            'order': 1,
            'checked': False,
            'photos': [
                {
                    'url': None,
                    'title': None,
                    'order': 1,
                },
                {
                    'url': None,
                    'title': None,
                    'order': 2,
                },
            ],
            'media': [],
        },
        {
            'id': 16239,
            'title': None,
            'description': None,
            'page_id': 90285,
            'created_at': '2024-04-02T11:09:50.000000Z',
            'updated_at': '2024-04-02T11:09:50.000000Z',
            'order': 2,
            'checked': False,
            'photos': [
                {
                    'url': None,
                    'title': None,
                    'order': 1,
                },
            ],
            'media': [],
        },
        {
            'id': 16240,
            'title': None,
            'description': None,
            'page_id': 90285,
            'created_at': '2024-04-02T11:09:50.000000Z',
            'updated_at': '2024-04-02T11:09:50.000000Z',
            'order': 3,
            'checked': False,
            'photos': [
                {
                    'url': None,
                    'title': None,
                    'order': 1,
                },
                {
                    'url': None,
                    'title': None,
                    'order': 2,
                },
            ],
            'media': [],
        },
        {
            'id': 16241,
            'title': None,
            'description': None,
            'page_id': 90285,
            'created_at': '2024-04-02T11:09:50.000000Z',
            'updated_at': '2024-04-02T11:09:50.000000Z',
            'order': 4,
            'checked': False,
            'photos': [],
            'media': [],
        },
    ],
    'page_information': [],
    'memorials': [],
    '_method': 'PUT',
}

    response = requests.post('https://memorycode.ru/api/page/30421140', json=json_data)


    return response.text

