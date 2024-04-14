# from Logging.LoggerConfig import logger
import requests

dir= 'b1g0voaeihj99r85mvoi' # TOdo: dir - зарезерироаное имя строеной функции, заменить
api= 'AQVNzuqpGnVZ97YTghU4nDOvG6ZRyW4AIG2mbs3f'


def block_model_1(prompt, block_main_question, main_question_ans):
    prompt = {
        "modelUri": f"gpt://{dir}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.3,
            "maxTokens": "5000"
        },

    
        "messages":  [
            {
                "role" : "system",
                "text" : f'''в твоем распоряжении имеется начальный вопрос на тему указанную ниже в квадратных скобках и ответ пользователя на него. 
                Ниже даны указания к контексту, на который ты должен опираться при выполнении задачи.
                Твоя задача составить 1 вопрос, который сможет навести пользователя на раскрытие делталей контекста.
                вопрос должен быть представлен без лишних деталей, ковычек и уточнений.
                Пример вопроса:
                Много ли было у него друзей? Поддерживал ли он связь с ними в дальнейшем? 

                [{prompt}]
                
                '''
            },
            {
                "role" : "assistant",
                "text" : block_main_question
            },
            {
                "role" : "user",
                "text" : main_question_ans
            }
        ]
                }
      
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {api}"}
    try:
        response = requests.post(url, headers=headers, json=prompt)
        result = response.json()
        
        return result["result"]["alternatives"][0]["message"]["text"]
    except Exception as e:
        # logger.debug(f"Ошибка в запросе к GPT в функции block1_model_1: {e}")
        return f"Ошибка : {response.status_code} или {e}"
    

def block_model_2(prompt, block_main_question, main_question_ans, second_question, second_answer):
    prompt = {
        "modelUri": f"gpt://{dir}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.3,
            "maxTokens": "5000"
        },

        "messages":  [
            {
                "role" : "system",
                "text" : f'''
                в твоем распоряжении имеется начальный вопрос на тему указанную ниже в квадратных скобках и ответ пользователя на него. 
                Ниже даны указания к контексту, на который ты должен опираться при выполнении задачи.
                Твоя задача составить 1 вопрос, который сможет навести пользователя на раскрытие делталей контекста.
                вопрос должен быть представлен без лишних деталей, ковычек и уточнений.
                Пример вопроса:
                Много ли было у него друзей? Поддерживал ли он связь с ними в дальнейшем? 

                [{prompt}]
                '''
            },
            {
                "role" : "assistant",
                "text" : block_main_question
            },
            {
                "role" : "user",
                "text" : main_question_ans
            },
            {
                "role" : "assistant",
                "text" : second_question
            },
            {
                "role" : "user",
                "text" : second_answer
            }

        ]
                }
      
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {api}"}
    try:
        response = requests.post(url, headers=headers, json=prompt)
        result = response.json()
        
        return result["result"]["alternatives"][0]["message"]["text"]
    except requests.exceptions as e:
        # logger.debug(f"Ошибка в запросе к GPT в функции block1_model_2: {e}")
        return f"Ошибка : {response.status_code} или {e}"
    
def sum(*answers, birth, death, name):
    messages = [
        {
            "role" : "system",
            "text" : f'''Ты модель, которая заточена под то, чтобы составлять полную биографию о человеке на основе отрывков
            рассказов другого человека. Тебе будет дано некоторое количество отрывков, которые ты должен будешь объединить  логически
            связный текст. Стоит учесть, что тект может являться результаотом распознавания голосовых, поэтому в нем могут присутствовать 
            лишние фразу, вставки слов паразитов и т.п. Нужно их удалить и сделать текст привлекательным для чтения.

            Тебе нужно будет разделить полученный и уже обработанный тект на три логические части и именовать их как
            1. вступление
            2. Продолжение
            3. Заключение 

            Как результат пользователю нужно выдать только биографию без каких либо замечаний, примечаний, вопросов, пометок.  выделать текст можно только
            разделяя его на абзацы и если хочешь сделать тект жирным, то обособляй его тегом <b>Какой-то текст</b>.

            Пользователю нужно увидеть в ответном сообщении только текст биографии, раздленных логичеки правильно, написанный красивым слаженным
            языком. 

            важное замечание, состоит втом, что ты не должен перетасовывать или дополнять факты, а только излагать данное тебе более красивым языком
            
            в рассказе ты будешь использовать имя героя биографии - {name},
            его дату рождения - {birth},
            его дату смерти - {death}
            '''
        }
    ]

    for i in answers:
        messages.append(
            {
                "role" : "user",
                "text" : i
            },
        )

    prompt = {
        "modelUri": f"gpt://{dir}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 1,
            "maxTokens": "10000"
        },
        "messages" : messages
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {api}"}
    try:
        response = requests.post(url, headers=headers, json=prompt)
        result = response.json()
        
        return result["result"]["alternatives"][0]["message"]["text"]
    except requests.exceptions as e:
        return f"Ошибка : {response.status_code} или {e}"


def epitath(bio):
    prompt = {
        "modelUri": f"gpt://{dir}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.2,
            "maxTokens": "5000" 
        },

    
        "messages":  [
            {
                "role" : "system",
                "text" : f'''
        Модель должна анализировать предоставленную биографическую информацию о человеке.
        На основе этой информации модель должна создать короткий текст, который мог бы использоваться как эпитафия на могиле или в памятнике усопшего.
        Эпитафия должна быть в стиле, подходящем для данной персоны, учитывая их достижения, характер, вклад в общество и т. д.
        Модель не должна добавлять никаких дополнительных комментариев, пометок или выделений текста в своем ответе. Она должна предоставить только эпитафию.

        Пример вывода:

        "Здесь покоится великий поэт Александр Сергеевич Пушкин,
        Который своими стихами в сердца вечно вплетал счастье и грусть.
        Его слова будут жить в наших сердцах навсегда,
        Как вечный источник вдохновения и мудрости."
        '''         
            }
        ]
                }
      
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {api}"}
    try:
        response = requests.post(url, headers=headers, json=prompt)
        result = response.json()
        
        return result["result"]["alternatives"][0]["message"]["text"]
    except Exception as e:
        # logger.debug(f"Ошибка в запросе к GPT в функции block1_model_1: {e}")
        return f"Ошибка : {response.status_code} или {e}"