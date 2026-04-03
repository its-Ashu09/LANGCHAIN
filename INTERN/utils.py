import fitz  # PyMuPDF
import re

def parse_pdf_filename(filename):
    pattern = r'(\d{4})_(\w+)_(\d+)_s(\d+)_(eng|hindi)\.pdf'
    match = re.match(pattern, filename)
    if match:
        year, month, day, shift, lang = match.groups()
        return int(year), month, int(day), int(shift), lang
    return None

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_accurate_answers(pdf_path):
    """
    Extracts 100% Accurate Answer Key using Visual Green Tick Detection
    """
    doc = fitz.open(pdf_path)
    accurate_map = {} 
    
    # Regex to find Metadata Box
    id_pattern = re.compile(
        r"Question ID\s*:\s*(\d+).*?Option 1 ID\s*:\s*(\d+).*?Option 2 ID\s*:\s*(\d+).*?Option 3 ID\s*:\s*(\d+).*?Option 4 ID\s*:\s*(\d+)", 
        re.DOTALL
    )

    for page in doc:
        # 1. Visual Green Tick Detection
        blocks = page.get_text("dict")["blocks"]
        green_indices = []
        blocks.sort(key=lambda b: b['bbox'][1]) # Sort vertically

        for b in blocks:
            if "lines" in b:
                for l in b["lines"]:
                    for s in l["spans"]:
                        color = s['color']
                        # Integer Color Check for Green
                        is_green = False
                        if isinstance(color, int):
                             r = (color >> 16) & 255
                             g = (color >> 8) & 255
                             b_val = color & 255
                             # If Green is dominant
                             if g > r and g > b_val and g > 50: 
                                 is_green = True
                        
                        if is_green:
                            txt = s['text'].strip()
                            # Check for "1.", "2.", "3.", "4."
                            m = re.match(r"^([1-4])[\.]?", txt)
                            if m:
                                green_indices.append(int(m.group(1)))

        # 2. Extract IDs
        page_text = page.get_text()
        matches = id_pattern.findall(page_text)
        
        # 3. Map Ticks to IDs
        for i, (qid, o1, o2, o3, o4) in enumerate(matches):
            if i < len(green_indices):
                idx = green_indices[i]
                correct_id = [o1, o2, o3, o4][idx-1]
                accurate_map[qid] = correct_id

    return accurate_map