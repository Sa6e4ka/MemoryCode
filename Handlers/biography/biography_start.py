from aiogram import F,Router,Bot
from aiogram.filters import StateFilter 
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from Logging.LoggerConfig import logger

from Auxiliary.states import (Page, 
                              Page18,  
                              Page45, 
                              Page60,
                              PageWAR)

# Table voice router 
trv = Router()


@trv.message(StateFilter(Page.state1), F.text)
async def table2(message : Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer('Напишите его(ее) дату рождения в формате ДД.ММ.ГГГГ')
    await state.set_state(Page.state2)
    

@trv.message(StateFilter(Page.state2), F.text)
async def table3(message : Message, state: FSMContext):
    try:
        if message.text[2] == '.' and message.text[5] == '.' and len(message.text) == 10 and int(message.text[0:2]) <= 31 and int(message.text[3:5]) <= 12:
            year = message.text[6:]
            print(year)
            await state.update_data(birth=message.text, year=year)

            await message.answer('Напишите его дату смерти в формате ДД.ММ.ГГГГ')    
            await state.set_state(Page.state13)
        else:
            await message.answer('Пожалуйста, введит дату в формате <b>ДД.ММ.ГГГГ</b>\n\nНапример - 04.07.2005')
    except:
        logger.debug('FUCK (table3)')
        await message.answer('Пожалуйста, введит дату в формате <b>ДД.ММ.ГГГГ</b>\n\nНапример - 04.07.2005')

@trv.message(StateFilter(Page.state13), F.text)
async def table3(message : Message, state: FSMContext):
    try:
        if message.text[2] == '.' and message.text[5] == '.' and len(message.text) == 10 and int(message.text[0:2]) <= 31 and int(message.text[3:5]) <= 12:
            await state.update_data(death=message.text)

            sd = await state.get_data()
            birth = sd['birth']

            lifelong = int(message.text[6:]) - int(birth[6:]) 
            await state.update_data(lifelong=lifelong)
            await message.answer('Напишите место, где он(она) родился')    

            await state.set_state(Page.state14)
    except Exception:
        logger.debug('FUCK (table4)')
        await message.answer('Пожалуйста, введите дату в формате <b>ДД.ММ.ГГГГ</b>\n\nНапример - 04.07.2005')


@trv.message(StateFilter(Page.state14), F.text)
async def table3(message : Message, state: FSMContext):
    try:
        await state.update_data(birthpalce=message.text)
        await message.answer('Напишите место, где он(она) умер')    

        await state.set_state(Page.state3)
    except Exception:
        logger.debug('FUCK (table4)')
        await message.answer('Похоже произошла ошибка')


@trv.message(StateFilter(Page.state3), F.text)
async def table4(message : Message, state: FSMContext):
    try:
        await state.update_data(deathplace=message.text)
        await message.answer('Загрузите фото')    

        await state.set_state(Page.state4)
    except Exception:
        logger.debug('FUCK (table4)')
        await message.answer('Пожалуйста, введит дату в формате <b>ДД.ММ.ГГГГ</b>\n\nНапример - 04.07.2005')


@trv.message(StateFilter(Page.state4), F.photo)
async def table5(message : Message, state: FSMContext, bot: Bot):
    try:
        # Также нужно будет добавить обрезание картинок
        file_path= f'photos/{message.chat.id}_photo.jpg'
        await bot.download(message.photo[-1].file_id, file_path)
        await state.update_data(photo= file_path)    
        await state.set_state(Page.state5)
       
        sd = await state.get_data()
        if sd['lifelong'] < 18 and sd['lifelong'] >= 0:
            block1_main_quest = 'Теперь биография.\n\nМожете ли вы рассказать о его(ее) запомнившихся вам чертах, какие из них были самыми яркими?\n\nКак он(она) влиял(а) на окружающих своей энегрией и характером?\n\n<b>Ответ можете отправить голосовым сообщением длиной не больше 30 секунд или написать текстом</b>'
           
            await message.answer(text=block1_main_quest)
            await state.set_state(Page18.state1)
            
            await state.update_data(block1_main_quest=block1_main_quest)

        elif sd['lifelong'] >= 18 and sd['lifelong'] < 45:
            block1_main_quest = 'Теперь биография.\n\nЕсли вы помните то, каким он(она) был(а) в детстве, то опишите черты его(ее) характера, которые выделялись с самого начала его(ее) жизненного пути. Как он(она) влияла на окружающих своей энергией?\nКак эти черты характера изменялись на протяжении всей его жизни?\nЭтот вопрос можно грубо перефразировать как "Опишите, каким он был"\n\n<b>Ответ можете отправить голосовым сообщением длиной не больше 30 секунд или написать текст</b>'
            
            await message.answer(text=block1_main_quest)
            await state.set_state(Page45.state1)

            await state.update_data(block1_main_quest=block1_main_quest)

        elif sd['lifelong'] >= 45 and sd['lifelong'] <= 150 and 1881 <= int(sd['year']) <= 1933:
            block1_main_quest = 'Теперь биография.\n\nОпишите черты характера человека, которые вам в нем(ней) хотелось бы особенно выделить.\nКак он(она) повлиял(а) на окружающих за cвою жизнь?\nЭтот вопрос можно грубо перефразировать как "Опишите, каким он(она) был(а)"\n\n<b>Ответ можете отправить голосовым сообщением продолжительностью не больше 30 секунд или написать текст</b>'
            
            await message.answer(text=block1_main_quest)
            await state.set_state(PageWAR.state1)

            await state.update_data(block1_main_quest=block1_main_quest)

        elif sd['lifelong'] >= 45 and sd['lifelong'] <= 150:
            block1_main_quest = 'Теперь биография.\n\n<b>Опишите черты его(ее) характера, которые выделялись на протяжении его(ее) жизненного пути. Как он(она) повлияла на окружающих за свою продолжительную жизнь?\n\nЭтот вопрос можно грубо перефразировать как \n"Опишите, каким он был"</b>\n\nОтвет можете отправить голосовым сообщением длиной не больше 30 секунд или написать текст'
            
            await message.answer(text=block1_main_quest)
            await state.set_state(Page60.state1)

            await state.update_data(block1_main_quest=block1_main_quest)
    
        else:
            await message.answer('Похоже, что вы ввели странные годы жизни человека.\n\nПожалуйста введите команду /page и повторите заполснение СП')
            await state.clear()
    except Exception as e:
       print(e)
       await message.answer('Похоже, что произошла непредвиденная ошибка.\n\nПожалуйста введите команду /page и попторите заполснение СП')



