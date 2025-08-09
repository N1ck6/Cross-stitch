import pdfplumber

def extract_raw_table_text(pdf_path, output_file):
    with pdfplumber.open(pdf_path) as pdf:
        all_text = []
        for page in pdf.pages:
            page_text = ""
            sorted_chars = sorted(page.chars, key=lambda c: (c["top"], c["x0"]))
            lines, current_line = [], []
            prev_top = None
            
            for char in sorted_chars:
                if prev_top is not None and abs(char["top"] - prev_top) > 5:
                    if current_line:
                        lines.append(current_line)
                    current_line = [char]
                else:
                    current_line.append(char)
                prev_top = char["top"]
            
            if current_line:
                lines.append(current_line)
            for line in lines:
                line_text = ""
                prev_x1 = None
                
                for char in line:
                    if prev_x1 is not None: # Spaces
                        space_count = max(0, int((char["x0"] - prev_x1) / 5))
                        line_text += " " * space_count
                    line_text += char["text"]
                    prev_x1 = char["x1"]
                
                page_text += line_text + "\n"
            
            all_text.append(page_text)
        for page in range(len(all_text)):
            all_text[page] = "\n".join(all_text[page].split('\n')[1:-1])
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(all_text))



pdf_file = 'input.pdf'
if not pdf_file:
    print("File not found")
    quit()
output_file = "output.txt"
extract_raw_table_text(pdf_file, output_file)
