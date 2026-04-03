import os
import json
import time
import uuid
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from .config import (
    ARCHIVE_BASE_DIR, ENGLISH_FOLDER, HINDI_FOLDER, OUTPUT_DIR, SUBJECTS
)
from .utils import parse_pdf_filename, extract_text_from_pdf, extract_accurate_answers
from .chain import get_chain

def get_pdf_pairs(num_pairs=50):
    """File matching logic"""
    english_path = Path(ARCHIVE_BASE_DIR) / ENGLISH_FOLDER
    hindi_path = Path(ARCHIVE_BASE_DIR) / HINDI_FOLDER
    
    english_pdfs = sorted([f for f in english_path.glob("*.pdf") if f.is_file()])
    pairs = []
    
    for eng_pdf in english_pdfs[:num_pairs]:
        eng_info = parse_pdf_filename(eng_pdf.name)
        if not eng_info: continue
        
        year, month, day, shift, _ = eng_info
        hindi_filename = f"{year}_{month}_{day:02d}_s{shift}_hindi.pdf"
        hindi_pdf = hindi_path / hindi_filename
        
        if hindi_pdf.exists():
            month_map = {'jan': '01', 'feb': '02', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12', 'mar':'03', 'apr':'04', 'may':'05', 'jun':'06', 'jul':'07', 'aug':'08'}
            m_num = month_map.get(month.lower(), '01')
            out_name = f"cgl_{day:02d}_{m_num}_{year}_shift_{shift}_tier1.json"
            
            pairs.append({
                'english': str(eng_pdf),
                'hindi': str(hindi_pdf),
                'output': out_name,
                'date': f"{day:02d}_{m_num}_{year}"
            })
    return pairs

def process_single_pair(pair):
    output_path = Path(OUTPUT_DIR) / pair['output']
    
    # Check Existance
    if output_path.exists():
        print(f"⏩ Skipping {pair['output']} (Already exists)")
        return

    print(f"🚀 Processing: {pair['output']}")
    
    try:
        # 1. EXTRACT RAW TEXT (Context for LLM)
        context_en = extract_text_from_pdf(pair['english'])
        context_hi = extract_text_from_pdf(pair['hindi'])
        
        # 2. EXTRACT ACCURATE ANSWER KEY (Python Logic)
        print(f"   🔍 Verifying Green Ticks via Python...")
        accurate_answers = extract_accurate_answers(pair['english'])
        print(f"   ✅ Found {len(accurate_answers)} verified answers.")

    except Exception as e:
        print(f"   ❌ Error reading files: {e}")
        return

    chain = get_chain()
    all_questions = []
    
    # 3. SUBJECT LOOP
    for subject in SUBJECTS:
        print(f"   📘 Subject: {subject}")
        
        # Process all 25 questions at once
        start_q, end_q = 1, 25
        num_q = end_q - start_q + 1
        print(f"      Processing all questions {start_q}-{end_q}...", end="", flush=True)
        try:
            result = chain.invoke({
                "subject_name": subject,
                "start_q": start_q,
                "end_q": end_q,
                "num_questions": num_q,
                "context_en": context_en, 
                "context_hi": context_hi
            })
            batch_qs = result.questions
            for q in batch_qs:
                q_dict = q.dict()
                q_dict['id'] = str(uuid.uuid4())
                if q_dict['qID'] in accurate_answers:
                    q_dict['answer']['correct_option_id'] = accurate_answers[q_dict['qID']]
                all_questions.append(q_dict)
            print(" Done.")
            time.sleep(2)
        except Exception as e:
            print(f" Error: {e}")
    
    # 4. DEDUPLICATION (By qID)
    unique_qs = {}
    for q in all_questions:
        if q['qID'] not in unique_qs:
            unique_qs[q['qID']] = q
            
    final_list = list(unique_qs.values())

    # 5. SAVE
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_list, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Saved {len(final_list)} questions to {output_path}")

# --- MAIN ENTRY ---
if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    pairs = get_pdf_pairs(num_pairs=50)
    print(f"Found {len(pairs)} pairs.")
    
    # Parallel Processing (Adjust max_workers based on your PC/API limits)
    with ThreadPoolExecutor(max_workers=1) as executor:
        executor.map(process_single_pair, pairs)