import requests 
import time
import json
# key id = ajeetakhktapuur170gl (name = API_GAY)

def short_files(file):
    headers = { 
        'Authorization': "API-key AQVNzuqpGnVZ97YTghU4nDOvG6ZRyW4AIG2mbs3f", 
        'Content-Type': 'application/x-www-form-urlencoded', 
    } 
    
    params = { 
        'topic': 'general', 
        'folderId': 'b1g0voaeihj99r85mvoi', 
        'lang' : 'ru' 
    } 
    
    with open(file, 'rb') as f: 
        data = f.read() 
    try:
        response = requests.post('https://stt.api.cloud.yandex.net/speech/v1/stt:recognize', params=params, headers=headers, data=data) 
        
        return response.json()['result']
    except:
        print(response.text)


def norm_files():

# YCAJEyyZ2kP8aoBruFlN1YT7D
# YCPn2RPAI-3XSZKGNV13Zq8OufxujIjI1WU06LK2

    # Укажите ваш IAM-токен и ссылку на аудиофайл в Object Storage.
    key = 't1.9euelZqJnJCZi8eRyImTy5uJk4mam-3rnpWayJmdyZCKnMmdm5WXnZfOmpjl9Pdddx9P-e9hNWTq3fT3HSYdT_nvYTVk6s3n9euelZqem5aRycmYzoudkM3NlMqWju_8zef1656VmpuVz86Nip2UlpaMnpOWis7H7_3F656Vmp6blpHJyZjOi52Qzc2UypaO.AufzKd2kWgMf0L6EssoaQ-FoAfYFvrJmogYRmBe3g_hV-AUCoCD0LRzOPmT0my-kZ3TIW2GBmiam9jcMNq2xAA'
    filelink = 'https://storage.yandexcloud.net/speechkitbucketforbot/Test.ogg'

    POST ='https://transcribe.api.cloud.yandex.net/speech/stt/v2/longRunningRecognize'

    body ={
        "config": {
            "specification": {
                "languageCode": "ru-RU"
            }
        },
        "audio": {
            "uri": filelink
        }
    }

    header = {'Authorization': 'Bearer {}'.format(key)}

    # Отправьте запрос на распознавание.
    req = requests.post(POST, headers=header, json=body)
    data = req.json()
    print(data)

    id = data['id']

   
    # Запрашивайте на сервере статус операции, пока распознавание не будет завершено.
    try:
        while True:
            
                time.sleep(1)

                GET = "https://operation.api.cloud.yandex.net/operations/{id}"
                req = requests.get(GET.format(id=id), headers=header)
                req = req.json()
                # print(req)
                if req['done']: break
                print("Not ready")
        # Покажите полный ответ сервaера в формате JSON.
        print("Response:")
        print(json.dumps(req, ensure_ascii=False, indent=2))

        # Покажите только текст из результатов распознавания.
        print("Text chunks:")
        for chunk in req['response']['chunks']:
            print(chunk['alternatives'][0]['text'])
    except KeyboardInterrupt:
        print('STOOP')
        pass
    
