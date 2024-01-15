import fitz  # PyMuPDF

input_pdf_path = 'input.pdf'
output_pdf_path = 'output22.pdf'
replacements = [
    ('PHANTOM', 'Gazprom'),
    ('13.01.2024', 'hello world'),
]

doc = fitz.open(input_pdf_path)

for page_num in range(len(doc)):
    page = doc[page_num]
    for old_text, new_text in replacements:
        text_instances = page.search_for(old_text)

        for inst in text_instances:
            # Add a rectangle to cover the old text
            # Change the fill color to match the page background if it's not white
            page.add_redact_annot(inst, fill=(1, 1, 1))
            # Apply redactions, which will remove the old text and fill the area with the background color
            page.apply_redactions()
            
            # Now insert the new text
            # Adjust the font size and position as needed
            # The 'align' parameter is set to 1 for center alignment
            page.insert_textbox(inst, new_text, fontname="helv", fontsize=11, align=1)

doc.save(output_pdf_path, garbage=4, deflate=True, clean=True)
doc.close()