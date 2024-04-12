from aiogram import F,Router, types, Bot
from aiogram.filters import Command ,StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.types.web_app_info import WebAppInfo
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from sqlalchemy.ext.asyncio import AsyncSession

from GPT import speechkit, promptedmodels


from Auxiliary.states import Page
from Auxiliary.keybaords import startKB

import time
import os

# Table voice router 
trv = Router()


@trv.callback_query(StateFilter(Page.state1), F.data == 'Голосовым вводом')
async def table1(call : CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer('Хорошо, сейчас вам будет задано несколько вопросов о человеке. Сначала введите имя, дату рождения и дату смерти вручную, а биографию состовим с помощью голосового ввода. Подробные инструкции будут даны чуть позже')
    time.sleep(2)
    await call.message.answer('Как звали человека?')

@trv.message(StateFilter(Page.state1), F.text)
async def table2(message : Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer('Напишите его дату рождения в формате ДД.ММ.ГГГГ')
    await state.set_state(Page.state2)
    
@trv.message(StateFilter(Page.state2), F.text)
async def table3(message : Message, state: FSMContext):
    await state.update_data(birth=message.text)

    await message.answer('Напишите его дату смерти в формате ДД.ММ.ГГГГ')    
    await state.set_state(Page.state3)

@trv.message(StateFilter(Page.state3), F.text)
async def table4(message : Message, state: FSMContext):
    await state.update_data(death=message.text)

    await message.answer('Загрузите фото')    
    await state.set_state(Page.state4)


@trv.message(StateFilter(Page.state4), F.photo)
async def table5(message : Message, state: FSMContext, bot: Bot):
    try:
        # Также нужно будет добавить обрезание картинок
        file_path= f'photos/{message.chat.id}_photo.jpg'
        await bot.download(message.photo[-1].file_id, file_path)
        await message.answer('Отлчино!\n\nТеперь биография\n\nРас   скажите о детстве и семейной жизни умершего человека. Какие были особенности его семьи и родителей?\n\nПостарайтесь изложить свой ответ в виде истории, а не отдельных фактов и отрывков.\n\n<b>Ответ отправьте голосовым сообщением длиной не больше 30 секунд</b>')
        await state.update_data(photo= file_path)    
        await state.set_state(Page.state5)
    except Exception as e:
       await message.answer(text=e)


@trv.message(StateFilter(Page.state5), F.voice)
async def table6(message : Message, state: FSMContext, bot: Bot):

    dir = f'voices/{message.chat.id}/'

    if not os.path.exists(dir):
        os.makedirs(dir)

    file_path = f'voices/{message.chat.id}/{message.chat.id}_1_voice.ogg'

    await bot.download(message.voice, file_path)
    await message.answer(text='Какие образование и профессиональный путь прошел у этого человека? Какие были его карьерные достижения и профессиональные интересы?')

    text = speechkit.short_files(file=file_path)

    await state.update_data(ans1=text)
    await state.set_state(Page.state6)


@trv.message(StateFilter(Page.state6), F.voice)
async def table6(message : Message, state: FSMContext, bot: Bot):

    file_path = f'voices/{message.chat.id}/{message.chat.id}_2_voice.ogg'

    await bot.download(message.voice, file_path)
    await message.answer(text='Какие были основные увлечения и хобби умершего человека? Чем он увлекался в свободное время?')

    text = speechkit.short_files(file=file_path)

    await state.update_data(ans2=text)
    await state.set_state(Page.state7)


@trv.message(StateFilter(Page.state7), F.voice)
async def table6(message : Message, state: FSMContext, bot: Bot):

    file_path = f'voices/{message.chat.id}/{message.chat.id}_3_voice.ogg'

    await bot.download(message.voice, file_path)
    await message.answer(text='Каковы были его вклады в общество или профессию? Участвовал ли он в каких-то общественных или благотворительных организациях?')

    text = speechkit.short_files(file=file_path)

    await state.update_data(ans3=text)
    await state.set_state(Page.state8)


@trv.message(StateFilter(Page.state8), F.voice)
async def table6(message : Message, state: FSMContext, bot: Bot):

    file_path = f'voices/{message.chat.id}/{message.chat.id}_4_voice.ogg'

    await bot.download(message.voice, file_path)
    await message.answer(text='Какие жизненные препятствия или вызовы пережил этот человек? Как он справлялся с трудностями?')

    text = speechkit.short_files(file=file_path)

    await state.update_data(ans4=text)
    await state.set_state(Page.state9)


@trv.message(StateFilter(Page.state9), F.voice)
async def table6(message : Message, state: FSMContext, bot: Bot):

    file_path = f'voices/{message.chat.id}/{message.chat.id}_5_voice.ogg'

    await bot.download(message.voice, file_path)
    await message.answer(text='Расскажите о его семейной жизни. Был ли у него супруг(а), дети, внуки? Какие были особенности его отношений в семье?')

    text = speechkit.short_files(file=file_path)

    await state.update_data(ans5=text)
    await state.set_state(Page.state10)


@trv.message(StateFilter(Page.state10), F.voice)
async def table6(message : Message, state: FSMContext, bot: Bot):

    file_path = f'voices/{message.chat.id}/{message.chat.id}_6_voice.ogg'

    await bot.download(message.voice, file_path)
    await message.answer(text='Какими были его убеждения и ценности? Есть ли какие-то принципы, которыми он руководствовался в жизни?')

    text = speechkit.short_files(file=file_path)

    await state.update_data(ans6=text)
    await state.set_state(Page.state11)


@trv.message(StateFilter(Page.state11), F.voice)
async def table6(message : Message, state: FSMContext, bot: Bot):

    file_path = f'voices/{message.chat.id}/{message.chat.id}_7_voice.ogg'

    await bot.download(message.voice, file_path)
    await message.answer(text='Каково было его наследие или влияние на окружающих? Как он будет помнен и чем запомнится людям?')

    text = speechkit.short_files(file=file_path)

    await state.update_data(ans7=text)
    await state.set_state(Page.state12)


@trv.message(StateFilter(Page.state12), F.voice)
async def table6(message : Message, state: FSMContext, bot: Bot):

    file_path = f'voices/{message.chat.id}/{message.chat.id}_8_voice.ogg'

    await bot.download(message.voice, file_path)
    text = speechkit.short_files(file=file_path)

    await state.update_data(ans8=text)

    sd = await state.get_data()
    resp = promptedmodels.sum(
        sd['ans1'],
        sd['ans2'],
        sd['ans3'],
        sd['ans4'],
        sd['ans5'],
        sd['ans6'],
        sd['ans7'],
        sd['ans8'], 
        name=sd['name'] 
    )

    await message.answer(text=resp)
    await state.clear()