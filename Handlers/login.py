from aiogram import F,Router
from aiogram.filters import Command ,StateFilter, or_f
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from aiogram.utils.keyboard import InlineKeyboardBuilder

from requests import exceptions

from Auxiliary.states import Start, Page
from Auxiliary.keybaords import resetKB, startKB

from Helps import login_to_pages
from Logging.LoggerConfig import logger

import time
# Login Router
lr = Router()

# Login states
login_email = Start.login_mail
login_password=  Start.login_password


@lr.message(StateFilter(None),Command('page'))
async def login_m(message: Message, state: FSMContext):
    await message.answer('Перед тем как создать страницу нужно войти\n\nЕсли у вас нет аккаунта то можете зарегистрироваться\n\nЕсли у вас уже есть аккаунт, то введите пожалуйста свою почту', reply_markup=resetKB.as_markup())
    await state.set_state(login_email)

@lr.callback_query(F.data == 'reset_Войти')
async def login_m_had(call : CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text(text='<b>Введите пожалуйста почту</b>')
    await state.set_state(login_email)

@lr.callback_query(F.data == 'start_Создать страницу памяти')
async def login_m_had(call : CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text(text='Перед тем как создать страницу нужно войти\n\nЕсли у вас нет аккаунта то можете зарегистрироваться\n\nЕсли у вас уже есть аккаунт, то введите пожалуйста свою почту', reply_markup=resetKB.as_markup())
    await state.set_state(login_email)


@lr.callback_query(StateFilter(login_email), F.data == 'reset_<< Назад')
async def login_m_had(call : CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer()
    await call.message.edit_text(text="Здравствуйте!\n\nЭто чат-бот от проекта <a href='https://memorycode.ru/'>memorycide.ru</a>\n\nЗдесь вы можете заполнить страницу памяти о человеке.", reply_markup=startKB.as_markup())


@lr.message(StateFilter(login_email), or_f(F.text, F.photo, F.audio, F.video, F.voice))
async def login_p(message: Message, state: FSMContext):
    if not message.text:
        await message.answer('Пожалуйста, напишите свою почту!')
    else:
        await state.update_data(mail=message.text)
        await message.answer('Теперь введите пароль')
        await state.set_state(login_password)


@lr.message(StateFilter(login_password), or_f(F.text, F.photo, F.audio, F.video, F.voice))
async def login_p_hand(message: Message, state: FSMContext):
    if not message.text:
        await message.answer('Пожалуйста, напишите введите пароль!')
    
    await state.update_data(password=message.text)
    sd = await state.get_data()
    try:
        data = login_to_pages.get_pages_from_email(login=sd['mail'], password=sd['password'])

        chKB = InlineKeyboardBuilder()
        for k, v in data[0].items():
            chKB.button(text=str(k), callback_data=f"pages_{v[0]}_{v[1]}")
        chKB.adjust(1,)

        await message.answer('Здравствуйте!\n\nвыберите страницу, которую хотите отредактировать', reply_markup=chKB.as_markup())
        
    except Exception as e:
        await message.answer(f'Похоже, что вы неправильно ввели логин или пароль.\n\nВведите логин или восстановите пароль или зарегистрируйтесь', reply_markup=resetKB.as_markup())
        await state.set_state(login_email)
        print(e)


@lr.callback_query(StateFilter(login_password), F.data.startswith("pages_"))
async def login_m_had(call : CallbackQuery, state: FSMContext):
    sd = await state.get_data()
    data1 = login_to_pages.get_pages_from_email(login=sd['mail'], password=sd['password'])
    page_id = call.data.split("_")[1]
    page_id_5 = call.data.split("_")[2]

    await call.answer()

    await state.set_state(Page.state1)
    await state.update_data(page_id=page_id, token=data1[1], page_id_5= page_id_5)

    s= await state.get_data()
    print(s)
    await call.message.edit_text(text=f"<b>Теперь приступим к заполнению страницы</b>\n\nвам будут поочередно задаваться вопросы по определенным блокам тем для составления биографии о вашем знакомом или родственнике.")
    time.sleep(1)
    await call.message.answer("<b>Как звали человека?</b>\n\nНапишите только его (ее) ФИО")