import fitz  

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
updated_replacements = [(item[0], input(f"Enter a value for {item[0]}: ")) for item in replacements]
updated_file_name = updated_replacements[0][1] + '_КП.pdf'

file_name = replacements[0][1] + '_КП.pdf'

replace_text_in_pdf('input.pdf', file_name, replacements)