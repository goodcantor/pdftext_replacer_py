import logging
import os
import fitz 
import re
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message, ChatType


def replace_text_in_pdf(input_pdf_path, output_pdf_path, replacements):
    print(f"Starting PDF modification: {input_pdf_path} -> {output_pdf_path}")
    
    if not os.path.exists(input_pdf_path):
        print(f"Error: Input PDF not found at {input_pdf_path}")
        raise FileNotFoundError(f"Input PDF not found: {input_pdf_path}")
        
    pdf_document = fitz.open(input_pdf_path)
    print(f"Opened PDF document with {len(pdf_document)} pages")
    
    regular = "regular.ttf"
    bold = "bold.ttf"
    
    if not os.path.exists(regular) or not os.path.exists(bold):
        print(f"Warning: Font files check - regular exists: {os.path.exists(regular)}, bold exists: {os.path.exists(bold)}")
    
    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        
        for search_text, replacement_text in replacements:
            text_instances = page.search_for(search_text)

            for inst in text_instances:                

                page.add_redact_annot(inst)

                page.apply_redactions()
                
                
                
                if ((search_text == "${client}") or (search_text == "${date}") or (search_text == "${result}")):
                  font=fitz.Font(fontname="F0", fontfile=bold)
                  
                  
                  text_length = font.text_length(replacement_text, 6.65)
                  
                  text_vertical_center = (inst[1] + inst[3]) / 2                
                  horizontal_position = inst[0] + 82 - (text_length / 2)
                  
                  if ((search_text == "${client}") or (search_text == "${date}")):
                    horizontal_position = inst[0]
                    
                  
                  new_position = (horizontal_position, text_vertical_center + 3)  
                  
                  page.insert_font(fontname="F0", fontbuffer=font.buffer)
                  if (search_text == "${result}"):
                    page.insert_text(new_position, replacement_text, fontsize=6.65, fontname='F0', color=(1, 1, 1))
                        
                  else: 
                    page.insert_text(new_position, replacement_text, fontsize=6.65, fontname='F0')         
                      
                else: 
                  font=fitz.Font(fontname="F1", fontfile=regular)
                  
                  text_length = font.text_length(replacement_text, 6.65)
                  
                  text_vertical_center = (inst[1] + inst[3]) / 2                
                  horizontal_position = inst[0] + 82 - (text_length / 2)
                  
                  new_position = (horizontal_position, text_vertical_center + 3)    
                  page.insert_font(fontname="F1", fontbuffer=font.buffer)

                  page.insert_text(new_position, replacement_text, fontsize=6.65, fontname='F1')
                  


    pdf_document.save(output_pdf_path)
    print(f"Saved modified PDF to {output_pdf_path}")
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
input_pdf_path = 'inputcenter.pdf'

logging.basicConfig(level=logging.INFO)

# TOKEN = '6493767052:AAGZtlLLfXnvOmEovU1FL8bBKYhP895WsTM'
TOKEN = '6615975703:AAGq2QiNCmaUVg52jR8oL0dhWDRS_MoPnhU'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

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

input_pdf_path = 'inputcenter.pdf'


def format_number(value):
    if re.match(r'^\d+(\.\d+)?$', value):
        num = float(value)
        formatted_num = "р. " + f"{num:,.2f}".replace(',', ' ').replace('.', ',')
        return formatted_num
    else:
        return value


async def process_replacements(text_items, user, chat_id):
    print(f"Starting process_replacements with {len(text_items)} items for chat_id: {chat_id}")
    
    if len(text_items) != len(replacements):
        print(f"Error: Expected {len(replacements)} items, got {len(text_items)}")
        await bot.send_message(chat_id, "Количество введенных данных не соответствует необходимому количеству замен.")
        return

    new_replacements = [(key, format_number(text.split(':', 1)[-1].strip()))
                        for (key, _), text in zip(replacements, text_items)]
    
    print(f"Created new_replacements: {new_replacements}")
    output_pdf_path = new_replacements[0][1] + '_КП.pdf'
    print(f"Output PDF path: {output_pdf_path}")

    try:
        replace_text_in_pdf(input_pdf_path, output_pdf_path, new_replacements)
        print("PDF generation completed")

        if not os.path.exists(output_pdf_path):
            print(f"Error: Generated PDF file not found at {output_pdf_path}")
            await bot.send_message(chat_id, "Ошибка: Не удалось создать PDF файл")
            return

        print(f"PDF file size: {os.path.getsize(output_pdf_path)} bytes")

        try:
            with open(output_pdf_path, "rb") as pdf_file:
                print("Sending notification to admin")
                await bot.send_message(1056198933, f"{user.full_name}\n{' '.join(text_items)}")
                
                print("Sending PDF document")
                await bot.send_document(chat_id, document=pdf_file)
                print("PDF sent successfully")
        except Exception as e:
            print(f"Error sending PDF: {str(e)}")
            await bot.send_message(chat_id, f"Ошибка при отправке файла: {str(e)}")
    except Exception as e:
        print(f"Error in PDF processing: {str(e)}")
        await bot.send_message(chat_id, f"Ошибка при обработке PDF: {str(e)}")
    finally:
        try:
            if os.path.exists(output_pdf_path):
                os.remove(output_pdf_path)
                print(f"Temporary PDF file removed: {output_pdf_path}")
        except Exception as e:
            print(f"Error removing temporary file: {str(e)}")


ALLOWED_USER_IDS = [189684105, 36995430, 700326689, 1056198933, 284867763]  

# Функция проверки пользователя
def is_user_allowed(user_id):
  return user_id in ALLOWED_USER_IDS

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
  if is_user_allowed(message.from_user.id):
    await message.reply("Привет! Пожалуйста, введи текст, разделяя его переносом, который вы хотите использовать для замены в PDF.")


@dp.message_handler(content_types=['text'], chat_type=ChatType.PRIVATE)
async def text_to_pdf_private(message: types.Message):
  if is_user_allowed(message.from_user.id):
    text_items = message.text.splitlines()
    await process_replacements(text_items, message.from_user, message.chat.id)


@dp.message_handler(content_types=['text'])
async def text_to_pdf_group(message: types.Message):
  if is_user_allowed(message.from_user.id):
    text_items = message.text.splitlines()
    await process_replacements(text_items, message.from_user, message.chat.id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    