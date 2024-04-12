from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.utils import executor
from Assests.voice_handler import from_ogg_to_text
API_TOKEN = '6794010217:AAHRB1AjLn2F6G9ytvsDWZt6Zdbp5iaBDJY'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Отправь мне голосовое сообщение, я сохраню его в формате ogg.")


@dp.message_handler(content_types=ContentType.VOICE)
async def voice_handler(message: types.Message):
    voice = message.voice
    file_id = voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_name = f'ogg_voice.ogg'
    await bot.download_file(file_path, file_name)
    await message.reply("Голосовое сообщение сохранено!")
    text = from_ogg_to_text(debug=True)
    await message.answer(text)


if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True)