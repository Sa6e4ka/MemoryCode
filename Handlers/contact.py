from aiogram import F,Router
from aiogram.filters import Command ,StateFilter, or_f
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from Auxiliary.states import Contact
from Auxiliary.keybaords import q_categoryKB

from Assests import memorycode_API_requests
from Logging.LoggerConfig import logger

# Contact Router
cr = Router()

name = Contact.name
mail = Contact.mail
phone = Contact.phone
q_category = Contact.q_category
question = Contact.question

@cr.message(Command('contact'))
async def contact1(message : Message, state: FSMContext):
    await message.answer('Здесь вы можете задать свой вопрос поддержке нашего сервиса\n\nПожалуйста введите свое имя')
    await state.set_state(name)
    
@cr.message(StateFilter(name), F.text)
async def contact1(message : Message, state: FSMContext):
    await state.update_data(name= message.text)
    await message.answer('Введите свою почту')
    await state.set_state(mail)

@cr.message(StateFilter(mail), F.text)
async def contact1(message : Message, state: FSMContext):
    await state.update_data(mail= message.text)
    await message.answer('Введите свой номер телефона')
    await state.set_state(phone)

@cr.message(StateFilter(phone), F.text)
async def contact1(message : Message, state: FSMContext):
    await state.update_data(phone= message.text)
    await message.answer('Выберите категорию вопроса', reply_markup=q_categoryKB.as_markup())
    await state.set_state(q_category)

@cr.callback_query(StateFilter(q_category))
async def contact1(call : CallbackQuery, state: FSMContext):
    await state.update_data(q_category= call.data)
    await call.answer()
    await call.message.answer(text='Опишите подробнее ваш вопрос')
    await state.set_state(question)
    

@cr.message(StateFilter(question), F.text)
async def contact1(message : Message, state: FSMContext):
    await state.update_data(question= message.text)
    await state.set_state(question)
    sd = await state.get_data()

    try:
        memorycode_API_requests.contact(name=sd['name'], email=sd['mail'], phone=sd['phone'],category=sd['q_category'], question=sd['question'])

        await message.answer('Ваш вопрос успешно отправлен поддержке нашего сервиса!')
    except Exception as e:
        await message.answer(
            f'Что-то пошло не так.\n\nПопробуйте позже {e}'
        )
