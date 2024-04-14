from aiogram import F,Router, Bot
from aiogram.filters import StateFilter, or_f
from aiogram.types import Message, CallbackQuery
from aiogram.types.web_app_info import WebAppInfo
from aiogram.fsm.context import FSMContext

from Database.orm_querry import history


from sqlalchemy.ext.asyncio import AsyncSession
from GPT import speechkit, promptedmodels
from Logging.LoggerConfig import logger
from Auxiliary.states import PageWAR
from Auxiliary.keybaords import epithKB, watch

from GPT.finalmodels import block_model_1,block_model_2, sum, epitath
from Helps.memorycode_API_requests import put
import os

wr = Router()

@wr.message(StateFilter(PageWAR.state1), or_f(F.voice, F.text))
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
            prompt='''
            Ты задаешь вопрос пользователю, который рассказывает об умершем человеке, который прошел 
            через великую отечественную войну. Перед тобой вопрос, на который
            ответил этот человек и сам ответ. Ты должен задать вопрос, который поможет пользователю раскрыть
            те детали характера, отношений с другими людьми (можешь иногад употреблять слово сослуживцы),  которые он не раскрылв ответе на предыдущий впорос.

            Твоя задача на данный момент с помощью одного вопроса раскрыть личностные качества человека, о котором рассказывает пользователь, опираясь при этом на контекст разговора
            '''
        )

        await message.answer(text=question2)
    
        await state.update_data(ans1=speechkit.short_files(file=file_path), block1_quest2=question2)
        await state.set_state(PageWAR.state2)

    elif message.text:

        sd = await state.get_data()

        question2 = block_model_1(
            block_main_question= sd['block1_main_quest'],
            main_question_ans= message.text,
            prompt='''
            Ты задаешь вопрос пользователю, который рассказывает об умершем человеке, который прошел 
            через великую отечественную войну. Перед тобой вопрос, на который
            ответил этот человек и сам ответ. Ты должен задать вопрос, который поможет пользователю раскрыть
            те детали характера, отношений с другими людьми (можешь иногад употреблять слово сослуживцы),  которые он не раскрылв ответе на предыдущий впорос.

            Твоя задача на данный момент с помощью одного вопроса раскрыть личностные качества человека, о котором рассказывает пользователь, опираясь при этом на контекст разговора

            '''
        )

        await message.answer(text=question2)
        await state.update_data(ans1=message.text, block1_quest2=question2)
        await state.set_state(PageWAR.state2)


@wr.message(StateFilter(PageWAR.state2), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/2_voice.ogg'
        await bot.download(message.voice, file_path)

        sd = await state.get_data()

        #Функция генерации вопроса
        question3 = block_model_2(
            block_main_question=sd['block1_main_quest'],
            main_question_ans = sd['ans1'],
            second_answer=speechkit.short_files(file=file_path),
            second_question=sd['block1_quest2'],
            prompt='''
            Ты задаешь вопрос пользователю, который рассказывает об умершем человеке, который прошел через великую отечественную войну
            Перед тобой есть два вопроса.
            на них уже ответил этот человек прежде, то есть ответы на них у тебя уже есть. 
            Ты должен задать вопрос об умершем человеке (в третьем лице), который поможет пользователю раскрыть те детали 
            личностных качеств  и характера человека, которые не были раскрыты ранее.

            Тебе нужно задать вопрос, который будет полностью раскрывать личность этого человека (напиминаю - в третьем лице)
            
                внимательно погрузись в контекст и подбери подходящий вопрос. НЕ повторяйся!

                Нужно, чтобы он был завершающим для составления части биографии умершего человека, посвященной его личностным качествам
                
                Избегай вопросов на тему смерти человека, задавай только те, которые касаются жизни, личных качеств, увлечений и т.п.
                Не задавай вопросы, которые также касаются нанесения увечий человеку
                Будь тактичным и вежливым в впоросе
                Будь внимателен в том, что тебе нежно предоставить только 1 вопрос пользователю вне зависимости от того, какой объем материала он тебе дал            
            ''')


        await message.answer(text= question3)
        await state.update_data(ans2=speechkit.short_files(file=file_path), block1_question3=question3)
        await state.set_state(PageWAR.state3)

    elif message.text:

        sd = await state.get_data()

        # Здесь будет функция генерации вопроса
        question3 = block_model_2(
            block_main_question=sd['block1_main_quest'],
            main_question_ans = sd['ans1'],
            second_answer=message.text,
            second_question=sd['block1_quest2'],
            prompt='''
            Ты задаешь вопрос пользователю, который рассказывает об умершем человеке, который прошел через великую отечественную войну
            Перед тобой есть два вопроса.
            на них уже ответил этот человек прежде, то есть ответы на них у тебя уже есть. 
            Ты должен задать вопрос об умершем человеке (в третьем лице), который поможет пользователю раскрыть те детали 
            личностных качеств  и характера человека, которые не были раскрыты ранее.

            Тебе нужно задать вопрос, который будет полностью раскрывать личность этого человека (напиминаю - в третьем лице)
            
                внимательно погрузись в контекст и подбери подходящий вопрос. НЕ повторяйся!

                Нужно, чтобы он был завершающим для составления части биографии умершего человека, посвященной его личностным качествам
                
                Избегай вопросов на тему смерти человека, задавай только те, которые касаются жизни, личных качеств, увлечений и т.п.
                Не задавай вопросы, которые также касаются нанесения увечий человеку
                Будь тактичным и вежливым в впоросе
                Будь внимателен в том, что тебе нежно предоставить только 1 вопрос пользователю вне зависимости от того, какой объем материала он тебе дал                    
            ''')


        await message.answer(text=question3)
        await state.update_data(ans2=message.text, block1_question3=question3)
        await state.set_state(PageWAR.state3)


@wr.message(StateFilter(PageWAR.state3), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/3_voice.ogg'
        await bot.download(message.voice, file_path)

        block2_main_quest = 'Теперь затронем личные отношения персонажа с другими людьми.\n\n<b>Расскажите о его(ее) семейных отношениях.\nКак он относился к свом родственникам?\nМного ли у него(ее) было друзей?\nвходили ли в их состав его(ее) сослуживцы?</b>\n\nПопытайтесь сформировать единую мысль, а не просто отвечайте на вопросы\nЭто поможет нейросети составить как можно более подробную биографию на основе изложенных фактов\n\n<b>Напоминаем, что в тестовом режиме доступна голосовая запись не длительностью не больше 30 секунд</b>'
        await message.answer(text=block2_main_quest)
        
        await state.update_data(ans3=speechkit.short_files(file=file_path), block2_main_quest=block2_main_quest)
        await state.set_state(PageWAR.state4)

    elif message.text:

        block2_main_quest = 'Теперь затронем личные отношения персонажа с другими людьми.\n\n<b>Расскажите о его(ее) семейных отношениях.\nКак он относился к свом родственникам?\nМного ли у него(ее) было друзей?\nвходили ли в их состав его(ее) сослуживцы?</b>\n\nПопытайтесь сформировать единую мысль, а не просто отвечайте на вопросы\nЭто поможет нейросети составить как можно более подробную биографию на основе изложенных фактов\n\n<b>Напоминаем, что в тестовом режиме доступна голосовая запись не длительностью не больше 30 секунд</b>'
        await message.answer(text=block2_main_quest)
        
        await state.update_data(ans3=message.text, block2_main_quest=block2_main_quest)
        await state.set_state(PageWAR.state4)


@wr.message(StateFilter(PageWAR.state4), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/4_voice.ogg'
        await bot.download(message.voice, file_path)
        
        sd = await state.get_data()

        # Функция генерации вопроса
        question2 = block_model_1(
            block_main_question= sd['block2_main_quest'],
            main_question_ans= speechkit.short_files(file=file_path),
            prompt='''Ты задаешь вопрос пользователю, который рассказывает об умершем человеке, который прошел через великую отечественную войну
            Перед тобой есть вопрос. Проанализируй  его и пойми контекст

            Ты должен задать новый вопрос, который поможет пользователю раскрыть
            те детали семейных, дружеских отношений человека с другими людьми. Если пользователь упоминал 
            в своем ответе на предыдущий впорос то, что у человека при жизни были внуки, 
            то обязательно задай вопрос о том, как он к ним относился. Удели больше внимания семейной жизни человека 
            его привязанностям к другим людям.

            Постарайся раскрыть те подтемы, которые пользователь не раскрыл в ответе на предыдущий впорос.
            Обязательно затронь семью человека, его брак. То насколько он счастлив в браке. О его отношениях с братьями, сестрами, если
            они были и эти темы не упоминались в разговре ранее.

            Будь тактичным, не задавай мрачно окрашенных эмоционально вопросов, это модет испугать пользователя
            Будь доброжелателен и, не касайся темы смерти человека в вопросах.

            Будь внимателен в том, что тебе нежно предоставить только 1 вопрос пользователю вне зависимости от того, какой объем материала он тебе дал
            ''')
        
        await message.answer(text=question2)

        await state.update_data(ans4=speechkit.short_files(file=file_path), block2_quest2=question2)
        await state.set_state(PageWAR.state5)

    elif message.text:

        sd = await state.get_data()
    
        question2 = block_model_1(
            block_main_question= sd['block2_main_quest'],
            main_question_ans= message.text,
            prompt='''Ты задаешь вопрос пользователю, который рассказывает об умершем человеке, который прошел через великую отечественную войну
            Перед тобой есть вопрос. Проанализируй  его и пойми контекст

            Ты должен задать новый вопрос, который поможет пользователю раскрыть
            те детали семейных, дружеских отношений человека с другими людьми. Если пользователь упоминал 
            в своем ответе на предыдущий впорос то, что у человека при жизни были внуки, 
            то обязательно задай вопрос о том, как он к ним относился. Удели больше внимания семейной жизни человека 
            его привязанностям к другим людям.

            Постарайся раскрыть те подтемы, которые пользователь не раскрыл в ответе на предыдущий впорос.
            Обязательно затронь семью человека, его брак. То насколько он счастлив в браке. О его отношениях с братьями, сестрами, если
            они были и эти темы не упоминались в разговре ранее.

            Будь тактичным, не задавай мрачно окрашенных эмоционально вопросов, это модет испугать пользователя
            Будь доброжелателен и, не касайся темы смерти человека в вопросах.

            Будь внимателен в том, что тебе нежно предоставить только 1 вопрос пользователю вне зависимости от того, какой объем материала он тебе дал
            ''')
        
        await message.answer(text=question2)

        await state.update_data(ans4=message.text, block2_quest2=question2)
        await state.set_state(PageWAR.state5)


@wr.message(StateFilter(PageWAR.state5), or_f(F.voice, F.text))
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
            Ты задаешь вопрос пользователю, который рассказывает об умершем человеке, прошедщем через великую отечественную войну
            Перед тобой есть два вопроса.
            на них уже ответил этот человек прежде, то есть ответы на них у тебя уже есть.  

            Ты должен задать новый вопрос, который поможет пользователю раскрыть
            те детали семейных, дружеских отношений человека с другими людьми. Если пользователь упоминал 
            в своем ответе на предыдущий впорос то, что у человека при жизни были внуки, 
            то обязательно задай вопрос о том, как он к ним относился. Удели больше внимания семейной жизни человека 
            его привязанностям к другим людям. 

            внимательно погрузись в контекст и подбери подходящий вопрос.

            нужно, чтобы он был завершающим для составления полной биографии о человеке
            Избегай вопросов на тему смерти человека, задавай только те, которые касаются жизни, личных качеств, увлечений и т.п.

            Не задавай вопросы, которые также касаются нанесения увечий человеку
            Будь тактичным и вежливым в впоросе
            Будь внимателен в том, что тебе нужно предоставить только 1 вопрос пользователю вне зависимости от того, какой объем материала он тебе дал
            '''
        )

        await message.answer(text=question3)

        await state.update_data(ans5=speechkit.short_files(file=file_path), block2_quest3=question3)
        await state.set_state(PageWAR.state6)

    elif message.text:

        sd = await state.get_data()

        question3 = block_model_2(
            block_main_question=sd['block2_main_quest'],
            main_question_ans = sd['ans4'],
            second_answer= message.text,
            second_question=sd['block2_quest2'],
            prompt='''
            Ты задаешь вопрос пользователю, который рассказывает об умершем человеке, прошедщем через великую отечественную войну
            Перед тобой есть два вопроса.
            на них уже ответил этот человек прежде, то есть ответы на них у тебя уже есть.  

            Ты должен задать новый вопрос, который поможет пользователю раскрыть
            те детали семейных, дружеских отношений человека с другими людьми. Если пользователь упоминал 
            в своем ответе на предыдущий впорос то, что у человека при жизни были внуки, 
            то обязательно задай вопрос о том, как он к ним относился. Удели больше внимания семейной жизни человека 
            его привязанностям к другим людям. 

            внимательно погрузись в контекст и подбери подходящий вопрос.

            нужно, чтобы он был завершающим для составления полной биографии о человеке
            Избегай вопросов на тему смерти человека, задавай только те, которые касаются жизни, личных качеств, увлечений и т.п.

            Не задавай вопросы, которые также касаются нанесения увечий человеку
            Будь тактичным и вежливым в впоросе
            Будь внимателен в том, что тебе нужно предоставить только 1 вопрос пользователю вне зависимости от того, какой объем материала он тебе дал
            '''
        )

        await message.answer(text=question3)
        await state.update_data(ans5=message.text, block2_quest3=question3)
        await state.set_state(PageWAR.state6)


@wr.message(StateFilter(PageWAR.state6), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/5_voice.ogg'
        await bot.download(message.voice, file_path)
        
        block3_main_q = 'Сейчас перейдем к блоку вопросов о военном опыте героя сегодняшней истории.\n\n<b>Расскажите как он проявил себя во времена великой отечественной войны\nОтличился ли он чем-то на службе\nРасскажите о его отношении с сослуживцами.\nО том как на его жизнь повлияла война.</b>\n\nНе забудьте уделить внимание деталям, которые, на первый взгляд могут оказаться мало значимыми, но это не так.\n\n<b>Напоминаем, что в тестовом режиме доступна голосовая запись не длительностью не больше 30 секунд</b>'

        await message.answer(text=block3_main_q)

        await state.update_data(ans6=speechkit.short_files(file=file_path), block3_main_q=block3_main_q)
        await state.set_state(PageWAR.state7)

    elif message.text:

        block3_main_q = 'Сейчас перейдем к блоку вопросов о военном опыте героя сегодняшней истории.\n\n<b>Расскажите как он проявил себя во времена великой отечественной войны\nОтличился ли он чем-то на службе\nРасскажите о его отношении с сослуживцами.\nО том как на его жизнь повлияла война.</b>\n\nНе забудьте уделить внимание деталям, которые, на первый взгляд могут оказаться мало значимыми, но это не так.\n\n<b>Напоминаем, что в тестовом режиме доступна голосовая запись не длительностью не больше 30 секунд</b>'

        await message.answer(text=block3_main_q)
        await state.update_data(ans6=message.text, block3_main_q=block3_main_q)
        await state.set_state(PageWAR.state7)


@wr.message(StateFilter(PageWAR.state7), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/5_voice.ogg'
        await bot.download(message.voice, file_path)
        
        sd = await state.get_data()
        # функция генерации вопроса о человеке на основе 
        # предыдущего вопроса (главного вопроса в блоке) - last_q 
        # и ответа пользователя на него - last_ans
        question2 = block_model_1(
            block_main_question= sd['block3_main_q'],
            main_question_ans= speechkit.short_files(file=file_path),
            prompt='''
            Ты задаешь вопрос пользователю, который рассказывает о человеке, прошедшем когда-то через великую отечественную войну. 
            Перед тобой вопрос, который был задан пользователю и ответ на него (со стороны пользователя). 
            Ты должен задать новый вопрос об умершем человеке (то есть в третьем лице), который поможет пользователю раскрыть детали, 
            касающиеся военного опыта этого человека. 

            вопрос может касаться подвигов человека, его отношений с сослуживцами, его отношеню долгу к службе

            Больше углубись в эмоциональоные аспекты и следи за контекстом.

            Опирайся на то, что пользователь рассказал тебе ранее!

            Постарайся раскрыть те подтемы, которые пользователь не раскрыл в ответе на предыдущий впорос.
            Путь его службы. То насколько он успешен в военном плане.

            Будь тактичным, не задавай мрачно окрашенных эмоционально вопросов, это модет испугать пользователя
            Будь доброжелателени, не касайся темы смерти человека в вопросах.

            Будь внимателен в том, что тебе нежно предоставить только 1 вопрос пользователю вне зависимости от того, какой объем материала он тебе дал
            ''')


        await message.answer(text=question2)

        await state.update_data(ans7=speechkit.short_files(file=file_path), block3_quest2=question2)
        await state.set_state(PageWAR.state8)

    elif message.text:
        sd = await state.get_data()

        question2 = block_model_1(
            block_main_question= sd['block3_main_q'],
            main_question_ans= message.text,
            prompt='''
            Ты задаешь вопрос пользователю, который рассказывает о человеке, прошедшем когда-то через великую отечественную войну. 
            Перед тобой вопрос, который был задан пользователю и ответ на него (со стороны пользователя). 
            Ты должен задать новый вопрос об умершем человеке (то есть в третьем лице), который поможет пользователю раскрыть детали, 
            касающиеся военного опыта этого человека. 

            вопрос может касаться подвигов человека, его отношений с сослуживцами, его отношеню долгу к службе

            Больше углубись в эмоциональоные аспекты и следи за контекстом.

            Опирайся на то, что пользователь рассказал тебе ранее!

            Постарайся раскрыть те подтемы, которые пользователь не раскрыл в ответе на предыдущий впорос.
            Путь его службы. То насколько он успешен в военном плане.

            Будь тактичным, не задавай мрачно окрашенных эмоционально вопросов, это модет испугать пользователя
            Будь доброжелателени, не касайся темы смерти человека в вопросах.

            Будь внимателен в том, что тебе нежно предоставить только 1 вопрос пользователю вне зависимости от того, какой объем материала он тебе дал
            ''')


        await message.answer(text=question2)
        await state.update_data(ans7=message.text, block3_quest2=question2)
        await state.set_state(PageWAR.state8)


@wr.message(StateFilter(PageWAR.state8), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/5_voice.ogg'
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
            Ты задаешь вопрос пользователю, который рассказывает об умершем человеке, прошедшем через великую отечественную войну. 
            Перед тобой есть два вопроса.
            на них уже ответил этот человек прежде, то есть ответы на них у тебя уже есть.  

            Ты должен задать новый вопрос об умершем человеке (то есть в третьем лице), который поможет пользователю раскрыть детали, 
            касающиеся военного опыта этого человека. 

            вопрос может касаться подвигов человека, его отношений с сослуживцами, его отношеню к долгу к службе

            Больше углубись в эмоциональоные аспекты и следи за контекстом.

            Опирайся на то, что пользователь рассказал тебе ранее!

            Постарайся раскрыть те подтемы, которые пользователь не раскрыл в ответе на предыдущий впорос.
            Путь его службы. То насколько он успешен в военном плане.

            Будь тактичным, не задавай мрачно окрашенных эмоционально вопросов, это модет испугать пользователя
            Будь доброжелателени, не касайся темы смерти человека в вопросах.

            Будь внимателен в том, что тебе нежно предоставить только 1 вопрос пользователю вне зависимости от того, какой объем материала он тебе дал         
            '''
        )

        await message.answer(text=question3)

        await state.update_data(ans8=speechkit.short_files(file=file_path), block3_quest3 = question3)
        await state.set_state(PageWAR.state9)

    elif message.text:
        sd = await state.get_data()

        question3 = block_model_2(
            block_main_question=sd['block3_main_q'],
            main_question_ans = sd['ans7'],
            second_answer= message.text,
            second_question=sd['block3_quest2'],
            prompt='''
            Ты задаешь вопрос пользователю, который рассказывает об умершем человеке, прошедшем через великую отечественную войну. 
            Перед тобой есть два вопроса.
            на них уже ответил этот человек прежде, то есть ответы на них у тебя уже есть.  

            Ты должен задать новый вопрос об умершем человеке (то есть в третьем лице), который поможет пользователю раскрыть детали, 
            касающиеся военного опыта этого человека. 

            вопрос может касаться подвигов человека, его отношений с сослуживцами, его отношеню к долгу к службе

            Больше углубись в эмоциональоные аспекты и следи за контекстом.

            Опирайся на то, что пользователь рассказал тебе ранее!

            Постарайся раскрыть те подтемы, которые пользователь не раскрыл в ответе на предыдущий впорос.
            Путь его службы. То насколько он успешен в военном плане.

            Будь тактичным, не задавай мрачно окрашенных эмоционально вопросов, это модет испугать пользователя
            Будь доброжелателени, не касайся темы смерти человека в вопросах.

            Будь внимателен в том, что тебе нежно предоставить только 1 вопрос пользователю вне зависимости от того, какой объем материала он тебе дал         
            '''
        )

        await message.answer(text=question3)
        await state.update_data(ans8=message.text, block3_quest3= question3)
        await state.set_state(PageWAR.state9)


@wr.message(StateFilter(PageWAR.state9), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/5_voice.ogg'
        await bot.download(message.voice, file_path)
        
        await message.answer(text='Хотели бы вы поделится чем-то, о чем мы вас еще не спросили?\n\nНе стесняйтесь говорить о своих личных переживаниях.\n\nЭто поможет нейросети понять то, как создать более качественную биографию на основе изложенных вами фактов.\n\n<b>Напоминаем, что в тестовом режиме доступна голосовая запись не длительностью не больше 30 секунд</b>')

        await state.update_data(ans9=speechkit.short_files(file=file_path))
        await state.set_state(PageWAR.state10)

    elif message.text:
        await message.answer(text='Хотели бы вы поделится чем-то, о чем мы вас еще не спросили?\n\nНе стесняйтесь говорить о своих личных переживаниях.\n\nЭто поможет нейросети понять то, как создать более качественную биографию на основе изложенных вами фактов\n\n<b>Напоминаем, что в тестовом режиме доступна голосовая запись не длительностью не больше 30 секунд</b>')
        await state.update_data(ans9=message.text)
        await state.set_state(PageWAR.state10)


@wr.message(StateFilter(PageWAR.state10), or_f(F.voice, F.text))
async def table6_1(message : Message, state: FSMContext, bot: Bot):
    if message.voice:

        file_path = f'voices/{message.chat.id}/5_voice.ogg'
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
        await state.update_data(sum=bio)

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
        await message.answer(text=f'Ваша биография:\n\n<b>{bio}</b>', reply_markup=epithKB.as_markup())
        # Здесь будет функция суммаризации ответов на вопросы 
        await state.update_data(sum=bio)


@wr.callback_query(StateFilter(PageWAR.state10),F.data=='Gen')
async def gen_epi(call : CallbackQuery, state: FSMContext):
    sd = await state.get_data()
    epith = epitath(bio=sd['bio'], name=sd['name'])
    await call.answer()
    await call.message.answer(f'Сгенерированная нейросетью эпитафия:\n\n<b>{epith}</b>\n\nТеперь напишите имя того, кого хотели бы считать автором эпитафии.')

    await state.update_data(epith=epith)
    await state.set_state(PageWAR.state11)

@wr.message(StateFilter(PageWAR.state11), F.text)
async def table6_11(message : Message, state: FSMContext, bot: Bot, session : AsyncSession):
    await state.update_data(auth_epi = message.text)
    s = await state.get_data()
    await message.answer('Эпитафия успешно сохранена!\n\nТеперь вы можете посмотреть страницу, нажав на кнопку', reply_markup=watch(id=s['page_id']))
    await history(session=session, data=s)
    put(s)

@wr.callback_query(StateFilter(PageWAR.state11), F.data=='Write')
async def gen_epi(call : CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer(f'Напишите свою эпитафию:')


@wr.message(StateFilter(PageWAR.state11), F.text)
async def table6_11(message : Message, state: FSMContext, bot: Bot):
    await state.update_data(epitath = message.text)
    await message.answer('Напишите автора эпитафии\n\n(им можете стать вы или кто-то другой)')
    await state.set_state(PageWAR.state12)


@wr.message(StateFilter(PageWAR.state12), F.text)
async def table6_11(message : Message, state: FSMContext, session: AsyncSession):
    await state.update_data(auth_epi = message.text)    
    s = await state.get_data()
    await message.answer('Эпитафия успешно сохранена!\n\nТеперь вы можете посмотреть страницу, нажав на кнопку', reply_markup=watch(id=s['page_id']))
    await history(session=session, data=s)
    print(s)
    put(data=s)

