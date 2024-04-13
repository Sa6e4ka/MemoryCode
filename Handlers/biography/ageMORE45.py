from aiogram import F,Router, Bot
from aiogram.filters import StateFilter, or_f
from aiogram.types import Message
from aiogram.types.web_app_info import WebAppInfo
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession
from GPT import speechkit, promptedmodels
from Logging.LoggerConfig import logger
from Auxiliary.states import Page60

import os

mr21 = Router()

@mr21.message(StateFilter(Page60.state1), or_f(F.voice, F.text))
async def table6_0(message : Message, state: FSMContext, bot: Bot):
    if message.voice:
        dir = f'voices/{message.chat.id}/'
        if not os.path.exists(dir):
            os.makedirs(dir)
        file_path = f'voices/{message.chat.id}/1_voice.ogg'
        await bot.download(message.voice, file_path)

        sd = await state.get_data()

        block1_main_q = sd['block1_main_quest']
        last_ans = speechkit.short_files(file=file_path)
        # Здесь будет функция генерации вопроса
        question2='вопрос 2 о 45+ лет человеке (блок характера и личных качеств)'
        await message.answer(text=question2)
    
        await state.update_data(ans1=last_ans, block1_quest2=question2)
        await state.set_state(Page60.state2)

    elif message.text:

        sd = await state.get_data()

        block1_main_q = sd['block1_main_quest']
        last_ans = message.text

        question2='вопрос 2 о 45+ лет человеке (блок характера и личных качеств)'

        await message.answer(text=question2)
        await state.update_data(ans1=message.text, block1_quest2=question2)
        await state.set_state(Page60.state2)


@mr21.message(StateFilter(Page60.state2), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/2_voice.ogg'
        await bot.download(message.voice, file_path)

        sd = await state.get_data()

        pre_last_quest = sd['block1_main_quest']
        last_quest = sd['block1_quest2']

        pre_last_ans = sd['ans1']
        last_ans = speechkit.short_files(file=file_path)
        # Здесь будет функция генерации вопроса
        question3 = 'вопрос 3 о 45+ лет человеке (блок характера и личных качеств)'

        await message.answer(text= question3)
        await state.update_data(ans2=last_ans, block1_question3=question3)
        await state.set_state(Page60.state3)

    elif message.text:

        sd = await state.get_data()

        pre_last_quest = sd['block1_main_quest']
        last_quest = sd['block1_quest2']

        pre_last_ans = sd['ans1']
        last_ans = message.text
        # Здесь будет функция генерации вопроса
        question3 = 'вопрос 3 о 45+ лет человеке (блок характера и личных качеств)'

        await message.answer(text=question3)
        await state.update_data(ans2=message.text, block1_question3=question3)
        await state.set_state(Page60.state3)


@mr21.message(StateFilter(Page60.state3), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/3_voice.ogg'
        await bot.download(message.voice, file_path)

        block2_main_quest = 'Теперь затронем личные отношения персонажа с другими людьми.\n\n<b>Расскажите о его(ее) семейных отношениях. Были ли у него(ее) братья или сетры?\nБыли ли у него(ее) внуки? Расскажите, как он к ним относился?\nМного ли у него(ее) было друзей?\nНасколько теплые отношения у него с ними были?</b>\n\nПопытайтесь сформировать единую мысль, а не просто отвечайте на вопросы\nЭто поможет нейросети составить как можно более подробную биографию на основе изложенных фактов\n\n<b>Напоминаем, что в тестовом режиме доступна голосовая запись не длительностью не больше 30 секунд</b>'
        await message.answer(text=block2_main_quest)
        
        await state.update_data(ans3=speechkit.short_files(file=file_path), block2_main_quest=block2_main_quest)
        await state.set_state(Page60.state4)

    elif message.text:

        block2_main_quest = 'Теперь затронем личные отношения персонажа с другими людьми.\n\n<b>Расскажите о его(ее) семейных отношениях. Были ли у него(ее) братья или сетры?\nБыли ли у него(ее) внуки? Расскажите, как он к ним относился?\nМного ли у него(ее) было друзей?\nНасколько теплые отношения у него с ними были?</b>\n\nПопытайтесь сформировать единую мысль, а не просто отвечайте на вопросы\nЭто поможет нейросети составить как можно более подробную биографию на основе изложенных фактов\n\n<b>Напоминаем, что в тестовом режиме доступна голосовая запись не длительностью не больше 30 секунд</b>'
        await message.answer(text=block2_main_quest)
        
        await state.update_data(ans3=message.text, block2_main_quest=block2_main_quest)
        await state.set_state(Page60.state4)


@mr21.message(StateFilter(Page60.state4), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/4_voice.ogg'
        await bot.download(message.voice, file_path)
        
        sd = await state.get_data()

        last_quest = sd['block2_main_quest']
        last_ans = speechkit.short_files(file=file_path)

        # Функция генерации вопроса
        question2 = 'вопрос 5 о 45+ лет человеке (блок отношений с другими людьми)'
        await message.answer(text=question2)

        await state.update_data(ans4=last_ans, block2_quest2=question2)
        await state.set_state(Page60.state5)

    elif message.text:

        sd = await state.get_data()

        last_quest = sd['block2_main_quest']
        last_ans = message.text
    
        question2 = 'вопрос 5 о 45+ лет человеке (блок отношений с другими людьми)'
        await message.answer(text=question2)

        await state.update_data(ans4=message.text, block2_quest3=question2)
        await state.set_state(Page60.state5)


@mr21.message(StateFilter(Page60.state5), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/5_voice.ogg'
        await bot.download(message.voice, file_path)

        sd = await state.get_data()

        pre_last_quest = sd['block2_main_quest']
        last_quest = sd['block2_quest2']

        pre_last_ans = sd['ans4']
        last_ans = speechkit.short_files(file=file_path)
        
        question3='вопрос 6 о 45+ лет человеке (блок отношений с другими людьми)'

        await message.answer(text=question3)

        await state.update_data(ans5=last_ans, block2_quest3=question3)
        await state.set_state(Page60.state6)

    elif message.text:

        sd = await state.get_data()

        pre_last_quest = sd['block2_main_quest']
        last_quest = sd['block2_quest2']

        pre_last_ans = sd['ans4']
        last_ans = message.text

        # #########
        question3='вопрос 6 о 45+ лет человеке (блок отношений с другими людьми)'

        await message.answer(text=question3)

        await message.answer(text=question3)
        await state.update_data(ans5=message.text, block2_quest3=question3)
        await state.set_state(Page60.state6)


@mr21.message(StateFilter(Page60.state6), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/5_voice.ogg'
        await bot.download(message.voice, file_path)
        
        block3_main_q = 'Сейчас перейдем к блоку вопросов об образовании и профессиональной деятельности героя сегодняшней истории.\n\n<b>Расскажите его(ее) образовательный путь и о препятсвиях, пройденных на нем.\n\nБыла ли его работа связана с наукой?\nРасскажите о его отношении к работе, к коллегам.\nО том как ответсвенно он выполнял свой профессиональный долг.</b>\n\nНе забудьте уделить внимание деталям, которые, на первый взгляд могут оказаться мало значимыми, но это не так.\n\n<b>Напоминаем, что в тестовом режиме доступна голосовая запись не длительностью не больше 30 секунд</b>'

        await message.answer(text=block3_main_q)

        await state.update_data(ans6=speechkit.short_files(file=file_path), block3_main_q=block3_main_q)
        await state.set_state(Page60.state7)

    elif message.text:

        block3_main_q = 'Сейчас перейдем к блоку вопросов об образовании и профессиональной деятельности героя сегодняшней истории.\n\n<b>Расскажите его(ее) образовательный путь и о препятсвиях, пройденных на нем.\n\nБыла ли его работа связана с наукой?\nРасскажите о его отношении к работе, к коллегам.\nО том как ответсвенно он выполнял свой профессиональный долг.</b>\n\nНе забудьте уделить внимание деталям, которые, на первый взгляд могут оказаться мало значимыми, но это не так.\n\n<b>Напоминаем, что в тестовом режиме доступна голосовая запись не длительностью не больше 30 секунд</b>'

        await message.answer(text=block3_main_q)
        await state.update_data(ans6=message.text, block3_main_q=block3_main_q)
        await state.set_state(Page60.state7)


@mr21.message(StateFilter(Page60.state7), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/5_voice.ogg'
        await bot.download(message.voice, file_path)
        
        sd = await state.get_data()

        last_q = sd['block3_main_q']
        last_ans = speechkit.short_files(file=file_path)
        # функция генерации вопроса о человеке на основе 
        # предыдущего вопроса (главного вопроса в блоке) - last_q 
        # и ответа пользователя на него - last_ans
        question2 = 'вопрос 8 о 45+ лет человеке (блок образования)'

        await message.answer(text=question2)

        await state.update_data(ans7=last_ans, block3_quest2=question2)
        await state.set_state(Page60.state8)

    elif message.text:
        sd = await state.get_data()

        last_q = sd['block3_main_q']
        last_ans = message.text

        # функция генерации вопроса о человеке на основе 
        # предыдущего вопроса (главного вопроса в блоке) - last_q 
        # и ответа пользователя на него - last_ans
        question2 = 'вопрос 8 о 45+ лет человеке (блок образования)'

        await message.answer(text=question2)
        await state.update_data(ans7=message.text, block3_quest2=question2)
        await state.set_state(Page60.state8)


@mr21.message(StateFilter(Page60.state8), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/5_voice.ogg'
        await bot.download(message.voice, file_path)

        sd = await state.get_data()

        pre_last_q = sd['block3_main_q']
        last_q = sd['block3_quest2']

        pre_last_ans = sd['ans7']
        last_ans = speechkit.short_files(file=file_path)

        # функция генерации вопроса о человеке на основе 
        # предыдущих вопросов (главного вопроса в блоке) - last_q, pre_last_q
        # и ответов пользователя на неих - last_ans, pre_last_ans
        question3 = 'вопрос 9 о 45+ лет человеке (блок образования)'

        await message.answer(text=question3)

        await state.update_data(ans8=speechkit.short_files(file=file_path), block3_quest3 = question3)
        await state.set_state(Page60.state9)

    elif message.text:
        sd = await state.get_data()

        pre_last_q = sd['block3_main_q']
        last_q = sd['block3_quest2']

        pre_last_ans = sd['ans7']
        last_ans = message.text

        # функция генерации вопроса о человеке на основе 
        # предыдущих вопросов (главного вопроса в блоке) - last_q, pre_last_q
        # и ответов пользователя на неих - last_ans, pre_last_ans
        question3 = 'вопрос 9 о 16-30 лет человеке (блок образования)'

        await message.answer(text=question3)
        await state.update_data(ans8=message.text, block3_quest3= question3)
        await state.set_state(Page60.state9)


@mr21.message(StateFilter(Page60.state9), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/5_voice.ogg'
        await bot.download(message.voice, file_path)
        
        await message.answer(text='Хотели бы вы поделится чем-то, о чем мы вас еще не спросили?\n\nНе стесняйтесь говорить о своих личных переживаниях.\n\nЭто поможет нейросети понять то, как создать более качественную биографию на основе изложенных вами фактов.\n\n<b>Напоминаем, что в тестовом режиме доступна голосовая запись не длительностью не больше 30 секунд</b>')

        await state.update_data(ans9=speechkit.short_files(file=file_path))
        await state.set_state(Page60.state10)

    elif message.text:
        await message.answer(text='Хотели бы вы поделится чем-то, о чем мы вас еще не спросили?\n\nНе стесняйтесь говорить о своих личных переживаниях.\n\nЭто поможет нейросети понять то, как создать более качественную биографию на основе изложенных вами фактов\n\n<b>Напоминаем, что в тестовом режиме доступна голосовая запись не длительностью не больше 30 секунд</b>')
        await state.update_data(ans9=message.text)
        await state.set_state(Page60.state10)


@mr21.message(StateFilter(Page60.state10), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/5_voice.ogg'
        await bot.download(message.voice, file_path)
        await state.update_data(ans10=speechkit.short_files(file=file_path))

        sd = await state.get_data()

        print(sd)
        anslist = [sd['ans1'], sd['ans2'], sd['ans3'],  sd['ans4'], sd['ans5'], sd['ans6'], sd['ans7'], sd['ans8'], sd['ans9'], sd['ans10']]

        await message.answer(text='Ваша биография:\n\n<b>Тут предполагается какой-то текст, сгенерированный моделью</b>')
        # Здесь будет функция суммаризации ответов на вопросы 
        await state.update_data(sum='sum of smth')
        await state.clear()

    elif message.text:
        await state.update_data(ans10=message.text)

        sd = await state.get_data()

        print(sd)
        anslist = [sd['ans1'], sd['ans2'], sd['ans3'],  sd['ans4'], sd['ans5'], sd['ans6'], sd['ans7'], sd['ans8'], sd['ans9'], sd['ans10']]

        await message.answer(text='Ваша биография:\n\n<b>Тут предполагается какой-то текст, сгенерированный моделью</b>')
        # Здесь будет функция суммаризации ответов на вопросы 
        await state.update_data(sum='sum of smth')
        await state.clear()





