import json
import uuid
import time
import os
import re
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from google import genai
from google.genai import types

# ---------------- CONFIG ---------------- #

ARCHIVE_BASE_DIR = "SSC_CGL_ARCHIVE"
ENGLISH_FOLDER = "input"
HINDI_FOLDER = "input_hindi"
OUTPUT_DIR = "jsonData"

SUBJECTS = [
    "General Awareness",
    "Quantitative Aptitude",
    "English Comprehension",
    "General Intelligence & Reasoning"
]

MAX_RETRIES = 2
NUM_PDFS_TO_PROCESS = 1  # Set number of PDF pairs to process
MAX_CONCURRENT_PAIRS = 1  # Number of PDF pairs to process in parallel

# ---------------------------------------- #

# Thread-local storage for client instances
thread_local = threading.local()

def get_client():
    """Get or create a thread-local client instance."""
    if not hasattr(thread_local, 'client'):
        thread_local.client = genai.Client(
            api_key="AIzaSyAk0tg0bJ-PFFJ3p7kvlwJCProRWGL8YjQ",
            http_options={"api_version": "v1"}
        )
    return thread_local.client

BASE_PROMPT = """
Generate questions from BOTH attached SSC CGL Tier 1 papers using the PDFs as the ONLY source of truth.

SUBJECT: {SUBJECT_NAME}

Generate EXACTLY 25 questions for this subject.
The same questions must appear in both papers (order may differ; difficulty may vary).

STRICT RULES:
1. Output ONLY valid JSON. No explanation, no markdown, no extra text.
2. Use the EXACT JSON structure provided below.
3. Keep JSON compact (single-line output is acceptable).
4. English ("en") and Hindi ("hi") content MUST be present.
5. Solutions MUST be complete and logically correct in BOTH languages.
6. Do NOT include tables anywhere.
7. If a question is based on data interpretation, diagram, chart, table, or figure, set "is_image_based": true.
8. For non-image questions, set "is_image_based": false.
9. Do NOT generate image URLs.
10. Generate EXACTLY 25 questions.
11. Generate ONLY {SUBJECT_NAME} questions.
12. Question ID from the PDF MUST be used as "qID".
13. Option IDs from the PDF MUST be used.
14. "correct_option_id" MUST exactly match the option ID.
15. Stop generation cleanly if output limit is reached. Do NOT truncate JSON.

JSON FORMAT:
[
  {{
    "id":"randomUUID",
    "qID":"question id same as in pdf",
    "meta":{{
      "exam_name":"CGL",
      "year":2024,
      "tier":"Tier1",
      "subject":"{SUBJECT_NAME}",
      "topic":"TOPIC_NAME",
      "sub_topic":"SUB_TOPIC_NAME",
      "difficulty":"Easy | Medium | Hard",
      "languages":["en","hi"],
      "date":"{DATE}",
      "shift":"Shift time slot like 12:30 PM - 1:30 PM"
    }},
    "content":{{
      "question_text":{{
        "en":"English question",
        "hi":"Hindi question"
      }},
      "is_image_based":false
    }},
    "options":[
      {{"id":"optionID","text":{{"en":"...","hi":"..."}}}},
      {{"id":"optionID","text":{{"en":"...","hi":"..."}}}},
      {{"id":"optionID","text":{{"en":"...","hi":"..."}}}},
      {{"id":"optionID","text":{{"en":"...","hi":"..."}}}}
    ],
    "answer":{{
      "correct_option_id":"correct option ID",
      "solution_text":{{
        "en":"Step-by-step solution",
        "hi":"चरणबद्ध समाधान"
      }}
    }}
  }}
]

IMPORTANT:
If all 25 questions cannot be generated, STOP and return a valid, closed JSON array only.
"""

def parse_pdf_filename(filename):
    """Parse PDF filename to extract date and shift info.
    Example: '2024_sep_09_s1_eng.pdf' -> (2024, 'sep', 9, 1)
    """
    pattern = r'(\d{4})_(\w+)_(\d+)_s(\d+)_(eng|hindi)\.pdf'
    match = re.match(pattern, filename)
    if match:
        year, month, day, shift, lang = match.groups()
        return int(year), month, int(day), int(shift), lang
    return None

def generate_output_filename(year, month, day, shift):
    """Generate output filename in format: cgl_DD_MM_YYYY_shift_N_tier1.json"""
    # Convert month name to number
    month_map = {
        'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
        'may': '05', 'jun': '06', 'jul': '07', 'july': '07',
        'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
    }
    month_num = month_map.get(month.lower(), '01')
    return f"cgl_{day:02d}_{month_num}_{year}_shift_{shift}_tier1.json"

def get_pdf_pairs(english_dir, hindi_dir, num_pairs):
    """Get matching PDF pairs from English and Hindi directories."""
    english_path = Path(english_dir)
    hindi_path = Path(hindi_dir)
    
    # Get all English PDFs
    english_pdfs = sorted([f for f in english_path.glob("*.pdf") if f.is_file()])
    
    pairs = []
    for eng_pdf in english_pdfs[:num_pairs]:
        eng_info = parse_pdf_filename(eng_pdf.name)
        if not eng_info:
            continue
        
        year, month, day, shift, _ = eng_info
        # Find matching Hindi PDF
        hindi_filename = f"{year}_{month}_{day:02d}_s{shift}_hindi.pdf"
        hindi_pdf = hindi_path / hindi_filename
        
        if hindi_pdf.exists():
            output_filename = generate_output_filename(year, month, day, shift)
            month_map = {
                'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
                'may': '05', 'jun': '06', 'jul': '07', 'july': '07',
                'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
            }
            month_num = month_map.get(month.lower(), '01')
            pairs.append({
                'english': str(eng_pdf),
                'hindi': str(hindi_pdf),
                'output': output_filename,
                'date': f"{day:02d}_{month_num}_{year}",
                'year': year,
                'shift': shift
            })
        else:
            print(f"Warning: No matching Hindi PDF found for {eng_pdf.name}")
    
    return pairs

def generate_subject_questions(subject, paper1, paper2, date_str, client_instance=None):
    """Generate questions for a subject. Uses provided client or gets thread-local one."""
    if client_instance is None:
        client_instance = get_client()
    
    prompt = BASE_PROMPT.replace("{SUBJECT_NAME}", subject).replace("{DATE}", date_str)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"  [{subject}] Attempt {attempt}...")
            response = client_instance.models.generate_content(
                model="models/gemini-2.5-pro",
                contents=[
                    types.Content(role="user", parts=[paper1]),
                    types.Content(role="user", parts=[paper2]),
                    types.Content(role="user", parts=[types.Part(text=prompt)])
                ],
                config={
                    "temperature": 0.2,
                    "top_p": 0.9,
                    "top_k": 40,
                    "max_output_tokens": 655360
                }
            )
            raw_text = response.text.strip()
            print(f"  [{subject}] Response: {len(raw_text)} chars")
            
            # Remove markdown code blocks if present
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            raw_text = raw_text.strip()
            
            #print this raw_text to a file
            with open("raw_text.txt", "w") as f:
                f.write(raw_text)
                
            parsed = json.loads(raw_text)

            # Inject UUIDs if needed
            for q in parsed:
                if q.get("id") == "randomUUID":
                    q["id"] = str(uuid.uuid4())

            if len(parsed) == 0:
                raise ValueError("Empty JSON returned")

            return parsed

        except Exception as e:
            print(f"  [{subject}] Error: {e}")
            if attempt == MAX_RETRIES:
                raise RuntimeError(f"Failed for subject {subject}") from e
            time.sleep(2)

def format_time(seconds):
    """Format seconds into a human-readable time string."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"

def process_pdf_pair(pair, pair_idx, total_pairs):
    """Process a single PDF pair - can be run in parallel."""
    start_time = time.time()
    output_path = Path(OUTPUT_DIR) / pair['output']
    
    # Check if output already exists (with lock to avoid race conditions)
    if output_path.exists():
        print(f"[{pair_idx}/{total_pairs}] Skipping {pair['output']} - already exists")
        return {'status': 'skipped', 'pair': pair, 'output': pair['output'], 'time': 0}
    
    print(f"[{pair_idx}/{total_pairs}] Processing: {pair['output']} (Started at {time.strftime('%H:%M:%S')})")
    print(f"  English: {Path(pair['english']).name}")
    print(f"  Hindi: {Path(pair['hindi']).name}")
    
    # Get thread-local client
    client_instance = get_client()
    
    # Load PDFs
    try:
        with open(pair['english'], "rb") as f:
            paper1 = types.Part.from_bytes(
                data=f.read(),
                mime_type="application/pdf"
            )
        
        with open(pair['hindi'], "rb") as f:
            paper2 = types.Part.from_bytes(
                data=f.read(),
                mime_type="application/pdf"
            )
    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"  [{pair['output']}] Error loading PDFs: {e} (Time: {format_time(elapsed_time)})")
        return {'status': 'error', 'pair': pair, 'error': str(e), 'time': elapsed_time}
    
    # Generate questions for all subjects
    all_questions = []
    subject_times = {}
    for subject in SUBJECTS:
        subject_start_time = time.time()
        print(f"  [{pair['output']}][{subject}] Starting...")
        try:
            subject_questions = generate_subject_questions(
                subject, paper1, paper2, pair['date'], client_instance
            )
            subject_elapsed = time.time() - subject_start_time
            subject_times[subject] = subject_elapsed
            print(f"  [{pair['output']}][{subject}] Got {len(subject_questions)} questions (Time: {format_time(subject_elapsed)})")
            all_questions.extend(subject_questions)
            
            # Save after each subject to prevent data loss
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(all_questions, f, ensure_ascii=False, indent=2)
            print(f"  [{pair['output']}][{subject}] Saved progress ({len(all_questions)} total questions)")
            
            # Sleep for 2 minutes between subjects
            if subject != SUBJECTS[-1]:  # Don't sleep after last subject
                time.sleep(20)
        except Exception as e:
            elapsed_time = time.time() - start_time
            print(f"  [{pair['output']}][{subject}] Failed: {e} (Time: {format_time(elapsed_time)})")
            if output_path.exists():
                print(f"  [{pair['output']}] Progress saved to {output_path} with {len(all_questions)} questions")
            return {'status': 'error', 'pair': pair, 'error': str(e), 'questions': len(all_questions), 'time': elapsed_time}
        
        time.sleep(5)
    
    elapsed_time = time.time() - start_time
    print(f"[{pair_idx}/{total_pairs}] Completed: {pair['output']} ({len(all_questions)} total questions) - Time: {format_time(elapsed_time)}")
    print(f"  Subject breakdown: {', '.join([f'{s}: {format_time(t)}' for s, t in subject_times.items()])}")
    return {'status': 'success', 'pair': pair, 'output': pair['output'], 'questions': len(all_questions), 'time': elapsed_time, 'subject_times': subject_times}

# ---------------- MAIN ---------------- #

# Start overall timing
overall_start_time = time.time()

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Get PDF pairs
english_dir = Path(ARCHIVE_BASE_DIR) / ENGLISH_FOLDER
hindi_dir = Path(ARCHIVE_BASE_DIR) / HINDI_FOLDER

print(f"Scanning for PDF pairs...")
pdf_pairs = get_pdf_pairs(english_dir, hindi_dir, NUM_PDFS_TO_PROCESS)
print(f"Found {len(pdf_pairs)} PDF pairs to process")

if len(pdf_pairs) == 0:
    print("No PDF pairs found. Exiting.")
    exit(1)

# Filter out pairs that already exist
pairs_to_process = []
for idx, pair in enumerate(pdf_pairs, 1):
    output_path = Path(OUTPUT_DIR) / pair['output']
    if not output_path.exists():
        pairs_to_process.append((pair, idx, len(pdf_pairs)))
    else:
        print(f"[{idx}/{len(pdf_pairs)}] Skipping {pair['output']} - already exists")

if len(pairs_to_process) == 0:
    print("All PDF pairs already processed. Exiting.")
    exit(0)

print(f"\nProcessing {len(pairs_to_process)} PDF pairs with {MAX_CONCURRENT_PAIRS} concurrent workers...")

# Process PDF pairs in parallel
results = []
with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_PAIRS) as executor:
    # Submit all tasks
    future_to_pair = {
        executor.submit(process_pdf_pair, pair, idx, total): (pair, idx)
        for pair, idx, total in pairs_to_process
    }
    
    # Collect results as they complete
    for future in as_completed(future_to_pair):
        pair, idx = future_to_pair[future]
        try:
            result = future.result()
            results.append(result)
        except Exception as e:
            print(f"  [{pair['output']}] Exception occurred: {e}")
            results.append({'status': 'error', 'pair': pair, 'error': str(e)})

# Print summary
print(f"\n{'='*60}")
print(f"Processing Summary:")
print(f"{'='*60}")
successful = [r for r in results if r.get('status') == 'success']
skipped = [r for r in results if r.get('status') == 'skipped']
errors = [r for r in results if r.get('status') == 'error']
total_questions = sum(r.get('questions', 0) for r in successful)
total_time = sum(r.get('time', 0) for r in successful)
avg_time = total_time / len(successful) if successful else 0

print(f"Successful: {len(successful)}")
print(f"Skipped: {len(skipped)}")
print(f"Errors: {len(errors)}")
print(f"Total questions generated: {total_questions}")
print(f"\nTiming Statistics:")
print(f"  Total processing time: {format_time(total_time)}")
print(f"  Average time per paper: {format_time(avg_time)}")
if successful:
    min_time = min(r.get('time', 0) for r in successful)
    max_time = max(r.get('time', 0) for r in successful)
    print(f"  Fastest paper: {format_time(min_time)}")
    print(f"  Slowest paper: {format_time(max_time)}")
    print(f"\nIndividual Paper Times:")
    for r in successful:
        print(f"  - {r['output']}: {format_time(r.get('time', 0))}")
print(f"{'='*60}")
overall_elapsed_time = time.time() - overall_start_time
print(f"\nDone! Processed {len(pairs_to_process)} PDF pairs")
print(f"Total execution time: {format_time(overall_elapsed_time)}")
