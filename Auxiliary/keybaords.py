from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, WebAppInfo




FuckGoBack = InlineKeyboardBuilder()
FuckGoBack.button(text='<< Назад', callback_data='agree_<< Назад')
FuckGoBack.adjust(1,)


startKB = InlineKeyboardBuilder()

startKB.button(text='Создать страницу памяти', callback_data=f'start_Создать страницу памяти')
startKB.button(text='Информация о сервисе', web_app=WebAppInfo(url='https://memorycode.ru/page'))
# , message: Message
startKB.adjust(1,)

agreeKB = InlineKeyboardBuilder()
list = ['Согласен(на)', 'Не согласен(на)', '<< Назад']
for i in list:
    agreeKB.button(text=i, callback_data=f'agree_{i}')
agreeKB.adjust(2, 1)


resetKB = InlineKeyboardBuilder()
list = ['Войти', 'Забыл(а) пароль','Зарегистрироваться', '<< Назад']
for i in list:
    resetKB.button(text=i, callback_data=f'reset_{i}')
resetKB.adjust(1, 2, 1,)


resetKB2 = InlineKeyboardBuilder()
list = ['Регистрация','Восстановить пароль', 'Создать страницу памяти', ]
for i in list:
    resetKB2.button(text=i, callback_data=f'reset1_{i}')
resetKB2.adjust(1,2,1)

resetKB3 = InlineKeyboardBuilder()
resetKB3.button(text='В главное меню', callback_data=f'reset_<< Назад')
resetKB3.adjust(1,)

q_categoryKB = InlineKeyboardBuilder()
list = ['Что-то не работает','Помогите разобраться', 'Помогите разобраться', 'Регистрация партнера', 'Нужно больше страниц', 'Запросить права на страницу памяти']
for i in list:
    q_categoryKB.button(text=i, callback_data=i)
q_categoryKB.adjust(1,)

epithKB = InlineKeyboardBuilder()
epithKB.button(text='Сгенерировать эпитафию', callback_data='Gen')
epithKB.button(text='Написать эпитафию', callback_data='Write')
epithKB.adjust(1,)
