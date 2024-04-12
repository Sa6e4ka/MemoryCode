from aiogram import F,Router
from aiogram.filters import Command ,StateFilter, or_f
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from requests import exceptions

from Auxiliary.states import Start, Page
from Auxiliary.keybaords import resetKB, startKB, createKB

from Assests import memorycode_API_requests
from Logging.LoggerConfig import logger

# Login Router
lr = Router()

# Login states
login_email = Start.login_mail
login_password=  Start.login_password


@lr.message(StateFilter(None),Command('page'))
async def login_m(message: Message, state: FSMContext):
    await message.answer('Перед тем как создать страницу нужно войти\n\nЕсли у вас нет аккаунта то можете зарегистрироваться\n\nЕсли у вас уже есть аккаунт, то введите пожалуйста свою почту', reply_markup=resetKB.as_markup())
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
    else:
        await state.update_data(password=message.text)
        
        sd = await state.get_data()
        try:
            data = memorycode_API_requests.auth(login=sd['mail'], password=sd['password'])
            print(data)
            await message.answer(f'Здравствуйте, {data[1]}\n\nКак вы бы хотели заполнить страницу памяти?', reply_markup=createKB.as_markup())
            await state.set_state(Page.state1)
            await state.update_data(session=data[0])
        except:
            await message.answer(f'Похоже, что вы неправильно ввели логин или пароль.\n\nВведите логин или восстановите пароль или зарегистрируйтесь', reply_markup=resetKB.as_markup())
            await state.set_state(login_email)
