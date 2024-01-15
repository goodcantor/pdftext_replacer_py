import fitz  # PyMuPDF

def replace_text_in_pdf(input_pdf_path, output_pdf_path, replacements):
    # Open the PDF file
    pdf_document = fitz.open(input_pdf_path)
    
    # Iterate over each page in the PDF
    for page_number in range(len(pdf_document)):
        # Get the page
        page = pdf_document[page_number]
        
        # Iterate over each replacement tuple
        for search_text, replacement_text in replacements:
            # Search for each text in the page
            text_instances = page.search_for(search_text)
            
            # Go through each instance found and replace
            for inst in text_instances:
                # Use the redaction feature to remove the text without adding a colored rectangle.
                page.add_redact_annot(inst)
                # Apply the redaction
                page.apply_redactions()
                
                text_vertical_center = (inst[1] + inst[3]) / 2                
                new_position = (inst[0], text_vertical_center + 2)
                
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
                  

    # Save the modified PDF to the output path
    pdf_document.save(output_pdf_path)
    pdf_document.close()
    print(f"PDF text replaced and saved as '{output_pdf_path}'")

# Define the list of replacements where each tuple is (oldValue, newValue)
replacements = [
    ("${client}", 'hellow'),
    ("${date}", 'hellow'),
    ("${first}", 'hellow'),
    ("${second}", 'hellow'),
    ("${third}", 'hellow'),
    ("${fourth}", 'hellow'),
    ("${fiveth}", 'hellow'),
    ("${sixth}", 'hellow'),
    ("${seventh}", 'hellow'),
    ("${result}", 'hellow'),
]


# updated_replacements = [(item[0], input(f"Enter a value for {item[0]}: ")) for item in replacements]
# Replace the text in 'input.pdf' and save the result to 'output.pdf'
replace_text_in_pdf('input.pdf', 'output.pdf', replacements)