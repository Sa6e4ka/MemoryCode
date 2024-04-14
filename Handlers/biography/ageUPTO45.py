from aiogram import F,Router, Bot
from aiogram.filters import StateFilter, or_f
from aiogram.types import Message, CallbackQuery
from aiogram.types.web_app_info import WebAppInfo
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession
from GPT import speechkit, promptedmodels
from Logging.LoggerConfig import logger
from Auxiliary.states import Page45

from Auxiliary.keybaords import epithKB
from GPT.finalmodels import block_model_1, block_model_2, sum, epitath

from Helps.memorycode_API_requests import put
import os

mr12 = Router()

@mr12.message(StateFilter(Page45.state1), or_f(F.voice, F.text))
async def table6_0(message : Message, state: FSMContext, bot: Bot):
    if message.voice:
        dir = f'voices/{message.chat.id}/'
        if not os.path.exists(dir):
            os.makedirs(dir)
        file_path = f'voices/{message.chat.id}/1_voice.ogg'
        await bot.download(message.voice, file_path)

        sd = await state.get_data()
        
        question2 = block_model_1(
            block_main_question= sd['block1_main_quest'],
            main_question_ans= speechkit.short_files(file=file_path),
            prompt='''Ты задаешь вопрос человеку, который рассказывает об умершем человеке в возрасте от 18 до 45 лет. Перед тобой вопрос, который
            был задан человеку и ответ на него от его лица. Ты должен задать новый вопрос, который поможет пользователю раскрыть
            те детали характера, увлечений, отношений с другими людьми человека, которые он не раскрыл
            в ответе на предыдущий впорос.

            Будь тактичным, не задавай мрачно окрашенных эмоционально вопросов, это модет испугать пользователя
            Будь доброжелателени, не касайся темы смерти человека в вопросах.
            '''
        )

        await message.answer(text=question2)
    
        await state.update_data(ans1=speechkit.short_files(file=file_path), block1_quest2=question2)
        await state.set_state(Page45.state2)

    elif message.text:

        sd = await state.get_data()

        question2 = block_model_1(
            block_main_question= sd['block1_main_quest'],
            main_question_ans= message.text,
            prompt='''Ты задаешь вопрос человеку, который рассказывает об умершем человеке в возрасте от 18 до 45 лет. Перед тобой вопрос, который
            был задан человеку и ответ на него от его лица. Ты должен задать новый вопрос, который поможет пользователю раскрыть
            те детали характера, увлечений, отношений с другими людьми человека, которые он не раскрыл
            в ответе на предыдущий впорос.

            Будь тактичным, не задавай мрачно окрашенных эмоционально вопросов, это модет испугать пользователя
            Будь доброжелателени, не касайся темы смерти человека в вопросах.
            '''
        )

        await message.answer(text=question2)
        await state.update_data(ans1=message.text, block1_quest2=question2)
        await state.set_state(Page45.state2)


@mr12.message(StateFilter(Page45.state2), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/2_voice.ogg'
        await bot.download(message.voice, file_path)

        sd = await state.get_data()


        question3 = block_model_2(
            block_main_question=sd['block1_main_quest'],
            main_question_ans = sd['ans1'],
            second_answer= speechkit.short_files(file=file_path),
            second_question=sd['block1_quest2'],
            prompt='''Ты задаешь вопрос человеку, который рассказывает об умершем человеке в возрасте от 18 до 45 лет. Перед тобой есть два вопроса, 
            на которые ответил этот человек прежде и сами ответы на них. Ты должен задать вопрос, который поможет пользователю раскрыть
            детали те детали характера, увлечений, отношений с другими людьми человека, которые он не раскрыл
            в ответе на предыдущий вопорос. внимательно погрузись в контекст и подбери подходящий вопрос.
            нужно, чтобы он был завершающим для составления полной биографии о человеке
            Избегай вопросов на тему смерти человека, задавай только те, которые касаются жизни, личных качеств, увлечений и т.п.
            Не задавай вопросы, которые также касаются нанесения увечий человеку
            Будь тактичным и вежливым в вопросе'''
        )

        # Здесь будет функция генерации вопроса

        await message.answer(text= question3)
        await state.update_data(ans2=speechkit.short_files(file=file_path), block1_question3=question3)
        await state.set_state(Page45.state3)

    elif message.text:

        sd = await state.get_data()

        # Здесь будет функция генерации вопроса
        question3 = block_model_2(
            block_main_question=sd['block1_main_quest'],
            main_question_ans = sd['ans1'],
            second_answer= message.text,
            second_question=sd['block1_quest2'],
            prompt='''Ты задаешь вопрос человеку, который рассказывает об умершем человеке в возрасте от 18 до 45 лет. Перед тобой есть два вопроса, 
            на которые ответил этот человек прежде и сами ответы на них. Ты должен задать вопрос, который поможет пользователю раскрыть
            детали те детали характера, увлечений, отношений с другими людьми человека, которые он не раскрыл
            в ответе на предыдущий вопорос. внимательно погрузись в контекст и подбери подходящий вопрос.
            нужно, чтобы он был завершающим для составления полной биографии о человеке
            Избегай вопросов на тему смерти человека, задавай только те, которые касаются жизни, личных качеств, увлечений и т.п.
            Не задавай вопросы, которые также касаются нанесения увечий человеку
            Будь тактичным и вежливым в впоросе'''
        )

        await message.answer(text=question3)
        await state.update_data(ans2=message.text, block1_question3=question3)
        await state.set_state(Page45.state3)


@mr12.message(StateFilter(Page45.state3), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/3_voice.ogg'
        await bot.download(message.voice, file_path)

        block2_main_quest = 'Теперь затронем личные отношения персонажа с другими людьми.\n\n<b>Расскажите о его семейных отношениях. Были ли у него братьяРасскажите о том много у него(ее) было друзей.\nКак он к ним относился?\nРасскажите о его любовных отношениях.</b>\n\nДалее вам могут быть предложены вопросы с уточнением некоторых мелочей.\nОни помогут нейросети составить как можно более подробную биографию на основе изложенных фактов'
        await message.answer(text=block2_main_quest)
        
        await state.update_data(ans3=speechkit.short_files(file=file_path), block2_main_quest=block2_main_quest)
        await state.set_state(Page45.state4)

    elif message.text:

        block2_main_quest = 'Теперь затронем личные отношения персонажа с другими людьми.\n\n<b>Расскажите о его семейных отношениях. Были ли у него братья или сетра.\nРасскажите о том много у него(ее) было друзей.\nКак он к ним относился?\nРасскажите о его любовных отношениях.</b>\n\nДалее вам могут быть предложены вопросы с уточнением некоторых мелочей.\nОни помогут нейросети составить как можно более подробную биографию на основе изложенных фактов'
        await message.answer(text=block2_main_quest)
        
        await state.update_data(ans3=message.text, block2_main_quest=block2_main_quest)
        await state.set_state(Page45.state4)


@mr12.message(StateFilter(Page45.state4), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/4_voice.ogg'
        await bot.download(message.voice, file_path)
        
        sd = await state.get_data()

        # Функция генерации вопроса
        question2 = block_model_1(
            block_main_question= sd['block2_main_quest'],
            main_question_ans= speechkit.short_files(file=file_path),
            prompt='''Ты задаешь вопрос человеку, который рассказывает об умершем человеке в возрасте от 18 до 45 лет. Перед тобой вопрос, который
            был задан человеку и ответ на него от его лица. Ты должен задать новый вопрос, который поможет пользователю раскрыть
            те детали семейных, дружеских или любовных отношений человека с другими людьми.
            Постарайся раскрыть те подтемы, которые пользователь не раскрыл в ответе на предыдущий впорос.
            Обязательно затронь семью человека, его брак. То насколько он счастлив в браке. О его отношениях с братьями, сестрами, если
            они были и эти темы не упоминались в разговре ранее.

            Будь тактичным, не задавай мрачно окрашенных эмоционально вопросов, это модет испугать пользователя
            Будь доброжелателен и, не касайся темы смерти человека в вопросах.

            Будь внимателен в том, что тебе нежно предоставить только 1 вопрос пользователю вне зависимости от того, какой объем материала он тебе дал
            ''')
        
        await message.answer(text=question2)

        await state.update_data(ans4=speechkit.short_files(file=file_path), block2_quest2=question2)
        await state.set_state(Page45.state5)

    elif message.text:

        sd = await state.get_data()

        question2 = block_model_1(
            block_main_question= sd['block2_main_quest'],
            main_question_ans= message.text,
            prompt='''Ты задаешь вопрос человеку, который рассказывает об умершем человеке в возрасте от 18 до 45 лет. Перед тобой вопрос, который
            был задан человеку и ответ на него от его лица. Ты должен задать новый вопрос, который поможет пользователю раскрыть
            те детали семейных, дружеских или любовных отношений человека с другими людьми.
            Постарайся раскрыть те подтемы, которые пользователь не раскрыл в ответе на предыдущий впорос.
            Обязательно затронь семью человека, его брак. То насколько он счастлив в браке. О его отношениях с братьями, сестрами, если
            они были и эти темы не упоминались в разговре ранее.

            Будь тактичным, не задавай мрачно окрашенных эмоционально вопросов, это модет испугать пользователя
            Будь доброжелателени, не касайся темы смерти человека в вопросах.

            Будь внимателен в том, что тебе нежно предоставить только 1 вопрос пользователю вне зависимости от того, какой объем материала он тебе дал
            ''')
        await message.answer(text=question2)

        await state.update_data(ans4=message.text, block2_quest2=question2)
        await state.set_state(Page45.state5)


@mr12.message(StateFilter(Page45.state5), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/5_voice.ogg'
        await bot.download(message.voice, file_path)

        sd = await state.get_data()
        
        question3 = block_model_2(
            block_main_question=sd['block2_main_quest'],
            main_question_ans = sd['ans4'],
            second_answer= speechkit.short_files(file=file_path),
            second_question=sd['block2_quest2'],
            prompt='''
            Ты задаешь вопрос человеку, который рассказывает об умершем человеке в возрасте от 18 до 45 лет. Перед тобой есть два вопроса, 
            на которые ответил этот человек прежде и сами ответы на них. Ты должен задать вопрос, который поможет пользователю раскрыть
            детали те детали отношения человека с другими людьми, отношений с семьей, люовных отношений, брака
            отношения к детям и т.п., которые он не раскрыл в ответе на предыдущий вопорос. 
            внимательно погрузись в контекст и подбери подходящий вопрос.
            нужно, чтобы он был завершающим для составления полной биографии о человеке
            Избегай вопросов на тему смерти человека, задавай только те, которые касаются жизни, личных качеств, увлечений и т.п.
            Не задавай вопросы, которые также касаются нанесения увечий человеку
            Будь тактичным и вежливым в впоросе
            Будь внимателен в том, что тебе нежно предоставить только 1 вопрос пользователю вне зависимости от того, какой объем материала он тебе дал
            '''
        )

        await message.answer(text=question3)

        await state.update_data(ans5=speechkit.short_files(file=file_path), block2_quest3=question3)
        await state.set_state(Page45.state6)

    elif message.text:

        sd = await state.get_data()

        question3 = block_model_2(
            block_main_question=sd['block2_main_quest'],
            main_question_ans = sd['ans4'],
            second_answer= message.text,
            second_question=sd['block2_quest2'],
            prompt='''Ты задаешь вопрос человеку, который рассказывает об умершем человеке в возрасте от 18 до 45 лет. Перед тобой есть два вопроса, 
            на которые ответил этот человек прежде и сами ответы на них. Ты должен задать вопрос, который поможет пользователю раскрыть
            детали те детали характера, увлечений, отношений с другими людьми человека, которые он не раскрыл
            в ответе на предыдущий вопорос. внимательно погрузись в контекст и подбери подходящий вопрос.
            нужно, чтобы он был завершающим для составления полной биографии о человеке
            Избегай вопросов на тему смерти человека, задавай только те, которые касаются жизни, личных качеств, увлечений и т.п.
            Не задавай вопросы, которые также касаются нанесения увечий человеку
            Будь тактичным и вежливым в впоросе
            Будь внимателен в том, что тебе нежно предоставить только 1 вопрос пользователю вне зависимости от того, какой объем материала он тебе дал            
            '''
        )

        await message.answer(text=question3)
        await state.update_data(ans5=message.text, block2_quest3=question3)
        await state.set_state(Page45.state6)


@mr12.message(StateFilter(Page45.state6), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/6_voice.ogg'
        await bot.download(message.voice, file_path)
        
        block3_main_q = 'Сейчас перейдем к блоку вопросов об образовании и профессиональной деятельности героя сегодняшней истории.\n\n<b>Поведайте нам о том, как хорош он(она) был(а) в образовании.\nРасскажите его(ее) образовательный путь и о препятсвиях, пройденных на нем.\n\nРасскажите о его отношении к работе, к коллегам.\nО том как ответсвенно он выполнял свой профессиональный долг.</b>\n\nНе забудьте уделить внимание деталям, которые, на первый взгляд могут оказаться не значимыми, но это не так'

        await message.answer(text=block3_main_q)

        await state.update_data(ans6=speechkit.short_files(file=file_path), block3_main_q=block3_main_q)
        await state.set_state(Page45.state7)

    elif message.text:

        block3_main_q = 'Сейчас перейдем к блоку вопросов об образовании и профессиональной деятельности героя сегодняшней истории.\n\n<b>Поведайте нам о том, как хорош он(она) был(а) в образовании.\nРасскажите его(ее) образовательный путь и о препятсвиях, пройденных на нем.\n\nРасскажите о его отношении к работе, к коллегам.\nО том как ответсвенно он выполнял свой профессиональный долг.</b>\n\nНе забудьте уделить внимание деталям, которые, на первый взгляд могут оказаться не значимыми, но это не так'

        await message.answer(text=block3_main_q)
        await state.update_data(ans6=message.text, block3_main_q=block3_main_q)
        await state.set_state(Page45.state7)


@mr12.message(StateFilter(Page45.state7), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/7_voice.ogg'
        await bot.download(message.voice, file_path)
        
        sd = await state.get_data()

        # функция генерации вопроса о человеке на основе 
        # предыдущего вопроса (главного вопроса в блоке) - last_q 
        # и ответа пользователя на него - last_ans
        question2 = block_model_1(
            block_main_question= sd['block3_main_q'],
            main_question_ans= speechkit.short_files(file=file_path),
            prompt='''
            Ты задаешь вопрос человеку, который рассказывает об умершем человеке в возрасте от 18 до 45 лет. Перед тобой вопрос, который
            был задан человеку и ответ на него. Ты должен задать новый вопрос об умершем человеке (то есть в третьем лице), который поможет пользователю раскрыть
            те детали образовательной деятельности, образовательного пути, трудостей на нем, профессионального становления,
            пути его карьеры, его успехов и провалов на этом пути.

            Опирайся на то, что пользователь рассказал тебе ранее!

            Постарайся раскрыть те подтемы, которые пользователь не раскрыл в ответе на предыдущий впорос.
            Обязательно затронь семью человека, его брак. То насколько он счастлив в браке. О его отношениях с братьями, сестрами, если
            они были и эти темы не упоминались в разговре ранее.

            Будь тактичным, не задавай мрачно окрашенных эмоционально вопросов, это модет испугать пользователя
            Будь доброжелателени, не касайся темы смерти человека в вопросах.

            Будь внимателен в том, что тебе нежно предоставить только 1 вопрос пользователю вне зависимости от того, какой объем материала он тебе дал
            ''')

        await message.answer(text=question2)

        await state.update_data(ans7=speechkit.short_files(file=file_path), block3_quest2=question2)
        await state.set_state(Page45.state8)

    elif message.text:
        sd = await state.get_data()

        # функция генерации вопроса о человеке на основе 
        # предыдущего вопроса (главного вопроса в блоке) - last_q 
        # и ответа пользователя на него - last_ans
        question2 = block_model_1(
            block_main_question= sd['block3_main_q'],
            main_question_ans= message.text,
            prompt='''
            Ты задаешь вопрос пользователю, который рассказывает об умершем человеке в возрасте от 18 до 45 лет. Перед тобой вопрос, который
            был задан человеку и ответ на него. Ты должен задать новый вопрос об умершем человеке (то есть в третьем лице), который поможет пользователю раскрыть
            те детали образовательной деятельности, образовательного пути, трудостей на нем, профессионального становелния,
            пути его карьеры, его успехов и провалов на этом пути, которые не были раскрыты ранее

            Опирайся на то, что пользователь рассказал тебе ранее!

            Постарайся раскрыть те подтемы, которые пользователь не раскрыл в ответе на предыдущий впорос.
            Обязательно затронь семью человека, его брак. То насколько он счастлив в браке. О его отношениях с братьями, сестрами, если
            они были и эти темы не упоминались в разговре ранее.

            Будь тактичным, не задавай мрачно окрашенных эмоционально вопросов, это модет испугать пользователя
            Будь доброжелателени, не касайся темы смерти человека в вопросах.

            Будь внимателен в том, что тебе нежно предоставить только 1 вопрос пользователю вне зависимости от того, какой объем материала он тебе дал
            ''')

        await message.answer(text=question2)
        await state.update_data(ans7=message.text, block3_quest2=question2)
        await state.set_state(Page45.state8)


@mr12.message(StateFilter(Page45.state8), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/8_voice.ogg'
        await bot.download(message.voice, file_path)

        sd = await state.get_data()

        # функция генерации вопроса о человеке на основе 
        # предыдущих вопросов (главного вопроса в блоке) - last_q, pre_last_q
        # и ответов пользователя на неих - last_ans, pre_last_ans
        question3 = block_model_2(
            block_main_question=sd['block3_main_q'],
            main_question_ans = sd['ans7'],
            second_answer= speechkit.short_files(file=file_path),
            second_question=sd['block3_quest2'],
            prompt='''
            Ты задаешь вопрос человеку, который рассказывает об умершем человеке в возрасте от 18 до 45 лет. 
            Перед тобой есть два вопроса.
            на них уже ответил этот человек прежде и сами ответы на них. 
            Ты должен задать вопрос об умершем человеке (то есть в третьем лице), который поможет пользователю раскрыть те детали образовательной деятельности, образовательного пути, трудостей на нем, профессионального становелния,
            пути его карьеры, его успехов и провалов на этом пути, которые не были раскрыты ранее. 
            
            внимательно погрузись в контекст и подбери подходящий вопрос. НЕ повторяйся!

            Нужно, чтобы он был завершающим для составления полной биографии о человеке
            Избегай вопросов на тему смерти человека, задавай только те, которые касаются жизни, личных качеств, увлечений и т.п.
            Не задавай вопросы, которые также касаются нанесения увечий человеку
            Будь тактичным и вежливым в впоросе
            Будь внимателен в том, что тебе нежно предоставить только 1 вопрос пользователю вне зависимости от того, какой объем материала он тебе дал            
            '''
        )

        await message.answer(text=question3)

        await state.update_data(ans8=speechkit.short_files(file=file_path), block3_quest3 = question3)
        await state.set_state(Page45.state9)

    elif message.text:
        sd = await state.get_data()

        pre_last_q = sd['block3_main_q']
        last_q = sd['block3_quest2']

        pre_last_ans = sd['ans7']
        last_ans = message.text

        # функция генерации вопроса о человеке на основе 
        # предыдущих вопросов (главного вопроса в блоке) - last_q, pre_last_q
        # и ответов пользователя на неих - last_ans, pre_last_ans
        question3 = block_model_2(
            block_main_question=sd['block3_main_q'],
            main_question_ans = sd['ans7'],
            second_answer=message.text,
            second_question=sd['block3_quest2'],
            prompt='''
            Ты задаешь вопрос человеку, который рассказывает об умершем человеке в возрасте от 18 до 45 лет. 
            Перед тобой есть два вопроса.
            на них уже ответил этот человек прежде и сами ответы на них. 
            Ты должен задать вопрос об умершем человеке (в третьем лице), который поможет пользователю раскрыть те детали образовательной деятельности, образовательного пути, трудостей на нем, профессионального становелния,
            пути его карьеры, его успехов и провалов на этом пути, которые не были раскрыты ранее. 
            
            внимательно погрузись в контекст и подбери подходящий вопрос. НЕ повторяйся!

            Нужно, чтобы он был завершающим для составления полной биографии о человеке
            Избегай вопросов на тему смерти человека, задавай только те, которые касаются жизни, личных качеств, увлечений и т.п.
            Не задавай вопросы, которые также касаются нанесения увечий человеку
            Будь тактичным и вежливым в впоросе
            Будь внимателен в том, что тебе нежно предоставить только 1 вопрос пользователю вне зависимости от того, какой объем материала он тебе дал            
            ''')

        await message.answer(text=question3)
        await state.update_data(ans8=message.text, block3_quest3= question3)
        await state.set_state(Page45.state9)


@mr12.message(StateFilter(Page45.state9), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/9_voice.ogg'
        await bot.download(message.voice, file_path)
        
        await message.answer(text='Хотели бы вы поделится чем-то, о чем мы вас еще не спросили?\n\nНе стесняйтесь говорить о своих личных переживаниях.\n\nЭто поможет нейросети понять то, как создать более качественную биографию на основе изложенных вами фактов')

        await state.update_data(ans9=speechkit.short_files(file=file_path))
        await state.set_state(Page45.state10)

    elif message.text:
        await message.answer(text='Хотели бы вы поделится чем-то, о чем мы вас еще не спросили?\n\nНе стесняйтесь говорить о своих личных переживаниях.\n\nЭто поможет нейросети понять то, как создать более качественную биографию на основе изложенных вами фактов')
        await state.update_data(ans9=message.text)
        await state.set_state(Page45.state10)


@mr12.message(StateFilter(Page45.state10), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/10_voice.ogg'
        await bot.download(message.voice, file_path)
        await state.update_data(ans10=speechkit.short_files(file=file_path))

        sd = await state.get_data()

        print(sd)
        
        bio = sum(
            sd['ans1'], 
            sd['ans2'], 
            sd['ans3'],  
            sd['ans4'], 
            sd['ans5'], 
            sd['ans6'], 
            sd['ans7'], 
            sd['ans8'], 
            sd['ans9'], 
            sd['ans10'],
            name=sd['name'],
            birth=sd['birth'],
            death=sd['death'],
        )

        await message.answer(text=f'Ваша биография:\n\n<b>{bio}</b>', reply_markup=epithKB.as_markup())
        # Здесь будет функция суммаризации ответов на вопросы 
        await state.update_data(bio=bio)
        await state.clear()

    elif message.text:
        await state.update_data(ans10=message.text)

        sd = await state.get_data()

        print(sd)
        bio = sum(
            sd['ans1'], 
            sd['ans2'], 
            sd['ans3'],  
            sd['ans4'], 
            sd['ans5'], 
            sd['ans6'], 
            sd['ans7'], 
            sd['ans8'], 
            sd['ans9'], 
            sd['ans10'],
            name=sd['name'],
            birth=sd['birth'],
            death=sd['death'],
        )

        await message.answer(text=f'<b>Ваша биография:</b>\n\n{bio}\n\n<b>Теперь вы можете сгенерировать эпитафию или написать ее сами</b>', reply_markup=epithKB.as_markup())
        # Здесь будет функция суммаризации ответов на вопросы 
        await state.update_data(bio=bio)

@mr12.callback_query(StateFilter(Page45.state10),F.data=='Gen')
async def gen_epi(call : CallbackQuery, state: FSMContext):
    sd = await state.get_data()
    e =epitath(sd['bio'])
    await call.answer()
    await call.message.answer(f'Сгенерированная нейросетью эпитафия:\n\n<b>{e}</b>\n\nТеперь напишите имя того, кого хотели бы считать автором эпитафии.')

    await state.update_data(epitath=e)
    await state.set_state(Page45.state11)

@mr12.message(StateFilter(Page45.state11), F.text)
async def table6_11(message : Message, state: FSMContext, bot: Bot):
    await state.update_data(auth_epi = message.text)
    await message.answer('Эпитафия успешно сохранена!')
    s = await state.get_data()
    put(s)

@mr12.callback_query(StateFilter(Page45.state11), F.data=='Write')
async def gen_epi(call : CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer(f'Напишите свою эпитафию:')


@mr12.message(StateFilter(Page45.state11), F.text)
async def table6_11(message : Message, state: FSMContext, bot: Bot):
    await state.update_data(epitath = message.text)
    await message.answer('Напишите автора эпитафии\n\n(им можете стать вы или кто-то другой)')

    await state.set_state(Page45.state12)

@mr12.message(StateFilter(Page45.state12), F.text)
async def table6_12311(message : Message, state: FSMContext, bot: Bot):
    await state.update_data(auth_epi = message.text)
    await message.answer('Эпитафия успешно сохранена!')

    s = await state.get_data()
    print(s)

    put(data=s)
