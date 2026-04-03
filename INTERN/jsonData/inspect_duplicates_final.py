import json

file_path = r'c:\Users\ashut\OneDrive\Desktop\Intern\INTERNSHIP\jsonData\cgl_11_09_2024_shift_1_tier1.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Inspect Pairs
pairs = [("630680360061", "630680360060"), ("630680285666", "630680285667")]

print("--- DUPLICATE CONTENT INSPECTION ---")
for q1_id, q2_id in pairs:
    items = [x for x in data if str(x.get('qID')) in [q1_id, q2_id]]
    print(f"\nPair: {q1_id} vs {q2_id}")
    if not items:
        print("  Text: (Items not found)")
        continue

    for item in items:
        print(f"  ID: {item.get('qID')}")
        print(f"  Subject: {item.get('meta', {}).get('subject')}")
        print(f"  Text: {item.get('content', {}).get('question_text', {}).get('en')}")
        print(f"  Options: {[o.get('text', {}).get('en') for o in item.get('options', [])]}")
        print(f"  Answer: {item.get('answer', {}).get('correct_option_id')}")
