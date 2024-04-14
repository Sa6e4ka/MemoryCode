from aiogram import F,Router, Bot
from aiogram.filters import StateFilter, or_f
from aiogram.types import Message, CallbackQuery
from aiogram.types.web_app_info import WebAppInfo
from aiogram.fsm.context import FSMContext

from Database.orm_querry import history

from sqlalchemy.ext.asyncio import AsyncSession
from GPT import speechkit, promptedmodels
from Logging.LoggerConfig import logger
from Auxiliary.states import Page18
from Auxiliary.keybaords import epithKB, watch
from GPT.finalmodels import block_model_1, block_model_2, sum, epitath
import os

from Helps.memorycode_API_requests import put

chldr = Router()

@chldr.message(StateFilter(Page18.state1), or_f(F.voice, F.text))
async def table6_0(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        dir = f'voices/{message.chat.id}/'
        if not os.path.exists(dir):
            os.makedirs(dir)
        file_path = f'voices/{message.chat.id}/1_voice.ogg'
        await bot.download(message.voice, file_path)

        sd = await state.get_data()

        quest = block_model_1(
            block_main_question= sd['block1_main_quest'],
            main_question_ans= speechkit.short_files(file=file_path),
            prompt='''Ты задаешь вопрос человеку, который рассказывает об умершем до 18 лет ребенке. Перед вопрос на который
            ответил этот человек и сам собственно ответ. Ты должен задать вопрос, который поможет пользователю раскрыть
            детали те детали характера, увлечений, отношений с другими людьми ребенка, которые он не раскрыл
            в ответе на предыдущий впорос.
            '''
        )
        print(quest)
        # Здесь будет функция генерации вопроса
        await message.answer(text=quest)

        
        await state.update_data(ans1=speechkit.short_files(file=file_path), quest2=quest)
        await state.set_state(Page18.state2)

    elif message.text:
        sd = await state.get_data()

        quest = block_model_1(
            block_main_question= sd['block1_main_quest'],
            main_question_ans= message.text,
            prompt='''Ты задаешь вопрос человеку, который рассказывает об умершем до 18 лет ребенке. Перед вопрос на который
            ответил этот человек и сам собственно ответ. Ты должен задать вопрос, который поможет пользователю раскрыть
            детали те детали характера, увлечений, отношений с другими людьми ребенка, которые он не раскрыл
            в ответе на предыдущий впорос.
            '''
        )
        print(quest)
        # Здесь будет функция генерации вопроса
        await message.answer(text=quest)

        
        await state.update_data(ans1=message.text, quest2=quest)
        await state.set_state(Page18.state2)


@chldr.message(StateFilter(Page18.state2), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/2_voice.ogg'
        await bot.download(message.voice, file_path)

        sd = await state.get_data()

        quest = block_model_2(
            block_main_question=sd['block1_main_quest'],
            main_question_ans = sd['ans1'],
            second_answer= speechkit.short_files(file=file_path),
            second_question=sd['quest2'],
            prompt='''Ты задаешь вопрос человеку, который рассказывает об умершем до 18 лет ребенке. Перед тобой есть два вопроса, 
            на которые ответил этот человек и сами ответы. Ты должен задать вопрос, который поможет пользователю раскрыть
            детали те детали характера, увлечений, отношений с другими людьми ребенка, которые он не раскрыл
            в ответе на предыдущий вопорос. внимательно погрузись в контекст и подбери подходящий вопрос.
            нужно, чтобы он был завершающим для составления полной биографии о человеке
            Избегай вопросов на тему смерти человека, задавай только те, которые касаются жизни, личных качеств, увлечений и т.п.
            Не задавай вопросы, которые также касаются нанесения увечий человеку'''
        )
        # Здесь будет функция генерации вопроса
        await message.answer(text=quest) 

        await state.update_data(ans2=speechkit.short_files(file=file_path), quest3=quest)
        await state.set_state(Page18.state3)

    elif message.text:
        sd = await state.get_data()

        quest = block_model_2(
            block_main_question=sd['block1_main_quest'],
            main_question_ans = sd['ans1'],
            second_answer= message.text,
            second_question=sd['quest2'],
            prompt='''Ты задаешь вопрос человеку, который рассказывает об умершем до 18 лет ребенке. Перед тобой есть два вопроса, 
            на которые ответил этот человек и сами ответы. Ты должен задать вопрос, который поможет пользователю раскрыть
            детали те детали характера, увлечений, отношений с другими людьми ребенка, которые он не раскрыл
            в ответе на предыдущий вопорос. внимательно погрузись в контекст и подбери подходящий вопрос.
            нужно, чтобы он был завершающим для составления полной биографии о человеке
            Избегай вопросов на тему смерти человека, задавай только те, которые касаются жизни, личных качеств, увлечений и т.п.
            Не задавай вопросы, которые также касаются нанесения увечий человеку
            '''
        )
        # Здесь будет функция генерации вопроса
        await message.answer(text=quest) 

        await state.update_data(ans2=message.text, quest3=quest)
        await state.set_state(Page18.state3)


@chldr.message(StateFilter(Page18.state3), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/3_voice.ogg'
        await bot.download(message.voice, file_path)

        await message.answer(text='Хотели бы вы поделится чем-то, о чем мы вас еще не спросили?\n\nНе стесняйтесь говорить о своих личных переживаниях.\n\nЭто поможет нейросети понять то, как создать более качественную биографию на основе изложенных вами фактов')
        text = speechkit.short_files(file=file_path)

        await state.update_data(ans3=text)
        await state.set_state(Page18.state4)

    elif message.text:
        await message.answer('Хотели бы вы поделится чем-то, о чем мы вас еще не спросили?\n\nНе стесняйтесь говорить о своих личных переживаниях.\n\nЭто поможет нейросети понять то, как создать более качественную биографию на основе изложенных вами фактов')
        
        await state.update_data(ans3=message.text)
        await state.set_state(Page18.state4)


@chldr.message(StateFilter(Page18.state4), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/4_voice.ogg'
        await bot.download(message.voice, file_path)

        text = speechkit.short_files(file=file_path)

        sd = await state.get_data()
        
        sum_bio = sum(
            sd['ans1'],
            sd['ans2'],
            sd['ans3'],
            speechkit.short_files(file=file_path),
            birth=sd['birth'], 
            death=sd['death'],
            name=sd['name']
        )

        print(sum_bio)
        await message.answer(text=f'Ваша биография:\n\n<b>{sum_bio}</b>', reply_markup=epithKB.as_markup())

        await state.update_data(sum=sum_bio)

    elif message.text:
        
        sd = await state.get_data()
        
        sum_bio = sum(
            sd['ans1'],
            sd['ans2'],
            sd['ans3'],
            message.text,
            birth=sd['birth'], 
            death=sd['death'],
            name=sd['name']
        )

        print(sum_bio)
        await message.answer(text=f'Ваша биография:\n\n<b>{sum_bio}</b>',reply_markup=epithKB.as_markup())

        await state.update_data(sum=sum_bio)
        await state.clear()


@chldr.callback_query(StateFilter(Page18.state4),F.data=='Gen')
async def gen_epi(call : CallbackQuery, state: FSMContext):
    sd = await state.get_data()
    epith = epitath(sd['bio'], sd['name'])
    await call.answer()
    await call.message.answer(f'Сгенерированная нейросетью эпитафия:\n\n<b>{epith}</b>\n\nТеперь напишите имя того, кого хотели бы считать автором эпитафии.')

    await state.update_data(epith=epith)
    await state.set_state(Page18.state11)

@chldr.message(StateFilter(Page18.state11), F.text)
async def table6_11(message : Message, state: FSMContext, session: AsyncSession):
    await state.update_data(auth_epi = message.text)
    s = await state.get_data()
    await message.answer('Эпитафия успешно сохранена!\n\nТеперь вы можете посмотреть страницу, нажав на кнопку', reply_markup=watch(id=s['page_id']))
    await history(session=session, data=s)
    put(s)

@chldr.callback_query(StateFilter(Page18.state11), F.data=='Write')
async def gen_epi(call : CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer(f'Напишите свою эпитафию:')


@chldr.message(StateFilter(Page18.state11), F.text)
async def table6_11(message : Message, state: FSMContext, bot: Bot):
    await state.update_data(epitath = message.text)
    await message.answer('Напишите автора эпитафии\n\n(им можете стать вы или кто-то другой)')

    await state.set_state(Page18.state12)

@chldr.message(StateFilter(Page18.state12), F.text)
async def table6_11(message : Message, state: FSMContext, session: AsyncSession):
    await state.update_data(auth_epi = message.text)
    s = await state.get_data()
    await message.answer('Эпитафия успешно сохранена!\n\nТеперь вы можете посмотреть страницу, нажав на кнопку', reply_markup=watch(id=s['page_id']))
    await history(session=session, data=s)
    print(s)
    put(data=s)