#Импортируем нужные дополнительные модули
import os
import asyncio
from Logging.LoggerConfig import logger

# Импортируем нужные модули из aiogram
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import BotCommandScopeAllPrivateChats, Message
from aiogram.client.default import DefaultBotProperties


#Достаем токен бота и url базы данных из переменной окружения
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

# Имопртируем функцию создания базы данных  
try:
    from Database.engine import create_db, session_maker
except Exception as e:
    logger.error(f'Ошибка в запросе к sql: {e}')

#Из папки handlers импортируем все хендлеры 
from Handlers.start import sr
from Handlers.register import rr
from Handlers.login import lr
from Handlers.contact import cr
from Handlers.biography.biography_start import trv
from Handlers.biography.ageUPTO18 import chldr
from Handlers.biography.ageUPTO45 import mr12
from Handlers.biography.ageMORE45 import mr21
from Handlers.biography.WAR import wr
# Из папки common импортируем команды
from Auxiliary.commands import private


#Создаем объект бота (передаем ему режим парсига получаемых ответов)
bot= Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode='HTML'))
#Создаем объект диспетчера
dp = Dispatcher()

# Добавляем Middlewares 
    # Чтобы использовать не одно конкретное соб ытие, а любое можно заменить message на update
from Auxiliary.middleware import DataBaseSession

#Подключаем к диспетчеру все роутеры из содаваемых хендлеров.   
dp.include_routers(sr, rr, lr, cr,chldr , trv, mr12, mr21, wr) 


# Добавляем основные "глобальные" хендлеры
@dp.message(Command('state'))
async def state_get(message: Message, state: FSMContext):
    current_state = await state.get_state()
    await message.answer(
        text=f'Текущее состояние: {current_state}'
    )


# Команда очистки состояния
@dp.message(Command('stateclear'))
async def clear_state(message: Message, state: FSMContext):
    current_state = await state.get_state()
    await state.clear()
    clear_state = await state.get_state()
    await message.answer(f'Состояние <b>{current_state}</b> сменилось на <b>{clear_state}</b>')


#Запускаем бота, помещаем доступные апдейты в start_polling
# отключаем обработку незавершившихся запросов
# Подключаем базу данных
async def main():
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await create_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private,scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot,allowed_updates=dp.resolve_used_update_types())

# Запуск main
if __name__ == "__main__":
    try:   
        print("I'M ALIVE BIIIYYYAAAATCH")
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот остановлен!')
        pass
    except Exception as e:  
        logger.error(f'КРИТИЧЕСКАЯ ОШИБКА: {e}')