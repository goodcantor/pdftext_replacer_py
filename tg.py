import logging
import fitz 
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message
from fpdf import FPDF


def replace_text_in_pdf(input_pdf_path, output_pdf_path, replacements):
    pdf_document = fitz.open(input_pdf_path)
    
    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        
        for search_text, replacement_text in replacements:
            text_instances = page.search_for(search_text)

            for inst in text_instances:

                page.add_redact_annot(inst)

                page.apply_redactions()
                
                text_vertical_center = (inst[1] + inst[3]) / 2                
                new_position = (inst[0], text_vertical_center + 3)
                
                if ((search_text == "${client}") or (search_text == "${date}") or (search_text == "${result}")):
                  font=fitz.Font("hebo")  
                  page.insert_font(fontname="F0", fontbuffer=font.buffer)
                  if (search_text == "${result}"):
                    page.insert_text(new_position, replacement_text, fontsize=6.65, fontname='F0', color=(1, 1, 1))    
                  else: 
                    page.insert_text(new_position, replacement_text, fontsize=6.65, fontname='F0')         
                      
                else: 
                  font=fitz.Font("helv")  
                  page.insert_font(fontname="F1", fontbuffer=font.buffer)

                  page.insert_text(new_position, replacement_text, fontsize=6.65, fontname='F1')
                  


    pdf_document.save(output_pdf_path)
    pdf_document.close()
    print(f"PDF text replaced and saved as '{output_pdf_path}'")


replacements = [
    ("${client}", 'Google.com'),
    ("${date}", '16.01.2024'),
    ("${first}", 'p. 12 234,23'),
    ("${second}", 'p. 11 214,00'),
    ("${third}", 'p. 32 000,00'),
    ("${fourth}", 'p. 12 999,00'),
    ("${fiveth}", 'p. 12 234,12'),
    ("${sixth}", 'p. 42 234,23'),
    ("${seventh}", 'p. 15 234,23'),
    ("${result}", 'p. 13 234,23'),
]
file_name = replacements[0][1] + '_КП.pdf'
input_pdf_path = replacements[0][1] + '_КП.pdf'


# Конфигурация логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
TOKEN = '6729706623:AAFlZ_J9LFw9JKhgwO10JjW57pTUr2MHMUI'  
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Пожалуйста, введите текст, разделенный запятыми, который вы хотите использовать для замены в PDF.")

@dp.message_handler(content_types=['text'])
async def text_to_pdf(message: types.Message):
    user_text = message.text
    text_items = user_text.split(',')

    if len(text_items) != len(replacements):
        await message.reply("Количество введенных данных не соответствует необходимому количеству замен.")
        return

    new_replacements = [(pair[0], text.strip()) for pair, text in zip(replacements, text_items)]
    output_pdf_path = f'{message.from_user.id}_output.pdf'

    replace_text_in_pdf(input_pdf_path, output_pdf_path, new_replacements)

    with open(output_pdf_path, "rb") as pdf_file:
        await bot.send_document(message.chat.id, document=pdf_file)

    try:
        os.remove(output_pdf_path)
    except Exception as e:
        logging.error("Ошибка при удалении файла: %s", e)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)