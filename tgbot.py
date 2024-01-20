import logging
import fitz  
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message
from fpdf import FPDF


# Конфигурация логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
TOKEN = '6729706623:AAFlZ_J9LFw9JKhgwO10JjW57pTUr2MHMUI'  
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Команда start, которая предлагает пользователю ввести текст

# Команда start, которая предлагает пользователю ввести текст
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Пожалуйста, введите текст, разделенный запятыми, который вы хотите сохранить в PDF.")

# Обработчик для текстовых сообщений
@dp.message_handler(content_types=['text'])
async def text_to_pdf(message: types.Message):
    # Получаем текст от пользователя и разделяем его на элементы
    user_text = message.text
    text_items = user_text.split(',')

    # Создаем PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Добавляем каждый элемент массива в PDF
    for item in text_items:
        pdf.multi_cell(0, 10, item.strip())

    # Сохраняем PDF в файл
    pdf_output = f'{message.from_user.id}.pdf'
    pdf.output(pdf_output)

    # Отправляем PDF пользователю
    with open(pdf_output, "rb") as pdf_file:
        await bot.send_document(message.chat.id, document=pdf_file)

    # Удаляем файл после отправки
    try:
        os.remove(pdf_output)
    except Exception as e:
        logging.error("Ошибка при удалении файла: ", e)

if __name__ == '__main__':
    # Запускаем бота
    executor.start_polling(dp, skip_updates=True)