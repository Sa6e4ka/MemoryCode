from aiogram import F,Router
from aiogram.filters import Command ,StateFilter, or_f
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from requests import exceptions

from Auxiliary.states import Start
from Auxiliary.keybaords import agreeKB, resetKB, resetKB2, resetKB3, startKB, FuckGoBack

from Helps import memorycode_API_requests
from Logging.LoggerConfig import logger

# Register Router
rr = Router()

# Состояния регистрации
register1 = Start.register_name
register2 = Start.register_mail
register3 = Start.register_phone

# Reset password state
reset = Start.reset

# Login state
login_email = Start.login_mail


@rr.callback_query(or_f(F.data == 'start_Зарегистрироваться', F.data =='reset_Зарегистрироваться' ))
async def register_first2(call : CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer()
    await call.message.edit_text(text='<a href="https://memorycode.ru/assets/front/pdf/memorycode_processing_of_personal_data.pdf">Согласие на обработку персональных данных</a>', reply_markup=agreeKB.as_markup())


@rr.callback_query(or_f(F.data =='reset_Забыл(а) пароль', F.data == 'reset1_Восстановить пароль'))
async def register_reset1(call : CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text(text='Введить email, чтобы получить новый пароль', reply_markup=FuckGoBack.as_markup())
    await state.set_state(reset)


@rr.message(StateFilter(reset), or_f(F.text, F.photo, F.audio, F.video, F.voice))
async def register_second(message: Message, state: FSMContext):
    if not message.text:
        await message.answer('Пожалуйста, введите свою почту!')
    else:
        try:
            memorycode_API_requests.reset_password(email=message.text)
            await message.answer('Вам на почту было выслано письмо с новым паролем.\n\nТеперь вы можете создать страницу памяти', reply_markup=startKB.as_markup())
            await state.clear()
        except Exception as e:
            await message.answer(f'Похоже, что на этот email аккаунт еще не зарегистрирован {e}')


@rr.callback_query(F.data == 'agree_Согласен(на)')
async def register_agree(call : CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text(text='Введите пожалйста ваше имя', reply_markup=FuckGoBack.as_markup())
    await state.set_state(register1)


@rr.callback_query(F.data == 'agree_Не согласен(на)')
async def register_agree(call : CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer(text='Хорошо, тогда, боимся, что вы не сможете продолжить регистрацию')
    await state.clear()


@rr.callback_query(F.data == 'agree_<< Назад')
async def register_agree(call : CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text(text='Перед тем как создать страницу нужно войти\n\nЕсли у вас нет аккаунта то можете зарегистрироваться\n\nЕсли у вас уже есть аккаунт, то введите пожалуйста свою почту', reply_markup=resetKB.as_markup())
    await state.set_state(login_email)


@rr.message(StateFilter(register1), or_f(F.text, F.photo, F.audio, F.video, F.voice))
async def register_second(message: Message, state: FSMContext):
    if not message.text:
        await message.answer('Пожалуйста, напишите свое имя!')
    else:
        await state.update_data(name=message.text)
        await message.answer('Теперь введите свою почту')
        await state.set_state(register2)


@rr.message(StateFilter(register2), or_f(F.text, F.photo, F.audio, F.video, F.voice))
async def register_third(message: Message, state: FSMContext):
    if not message.text:
        await message.answer('Пожалуйста, напишите свою почту!')
    else:
        await state.update_data(mail=message.text)
        await message.answer('Теперь введите свой телефон в формате +7 777 777 77 77')
        await state.set_state(register3)


@rr.message(StateFilter(register3), or_f(F.text, F.photo, F.audio, F.video, F.voice))
async def register_fourth(message: Message, state: FSMContext):
    if not message.text or not message.text.startswith('+'):
        await message.answer('Пожалуйста, напишите свой телефон в формате <b>+7 777 777 77 77</b>')
    else:
        await state.update_data(phone=message.text)
        sd = await state.get_data()
        try:
            memorycode_API_requests.register(
                name=sd['name'],
                email= sd['mail'],
                phone=sd['phone']
            )
        except exceptions.ConnectionError:
            await message.answer('Спасибо!\n\nСейчас вам на почту придет письмо с паролем.\n\nИспользуйте команду', reply_markup=startKB.as_markup())
            logger.info('Новый пользователь')
            return
        
        await message.answer('Похоже, что аккаунт с данным email уже существует...\n\nПопробуйте зарегистрироваться еще раз или войдите', reply_markup=resetKB2.as_markup())
        await state.clear()


@rr.callback_query(F.data=='reset1_Регистрация')
async def reg_res(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text='<a href="https://memorycode.ru/assets/front/pdf/memorycode_processing_of_personal_data.pdf">Согласие на обработку персональных данных</a>', reply_markup=agreeKB.as_markup())

@rr.callback_query(F.data=='reset1_Создать страницу памяти')
async def reg_res(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text(text='Перед тем как создать страницу нужно войти\n\nВведите свою почту:', reply_markup=resetKB3.as_markup())
    await state.set_state(login_email)