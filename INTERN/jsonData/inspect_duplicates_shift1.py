import json

file_path = r'c:\Users\ashut\OneDrive\Desktop\Intern\INTERNSHIP\jsonData\cgl_11_09_2024_shift_1_tier1.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Pairs to check
pairs = [
    ("630680360061", "630680360060"),
    ("630680285666", "630680285667")
]

print("--- DUPLICATE CONTENT INSPECTION ---")

for q1_id, q2_id in pairs:
    print(f"\nExample Pair: {q1_id} vs {q2_id}")
    
    # Get items
    item1 = next((x for x in data if str(x.get('qID')) == q1_id), None)
    item2 = next((x for x in data if str(x.get('qID')) == q2_id), None)

    if not item1 or not item2:
        print("  One or both items not found.")
        continue

    # Print Item 1
    print(f"  [Item 1] ID: {item1.get('qID')} | Subject: {item1.get('meta', {}).get('subject')}")
    print(f"  Text: {item1.get('content', {}).get('question_text', {}).get('en')}")
    print(f"  Options: {[o.get('text', {}).get('en') for o in item1.get('options', [])]}")
    
    # Print Item 2
    print(f"  [Item 2] ID: {item2.get('qID')} | Subject: {item2.get('meta', {}).get('subject')}")
    print(f"  Text: {item2.get('content', {}).get('question_text', {}).get('en')}")
    print(f"  Options: {[o.get('text', {}).get('en') for o in item2.get('options', [])]}")
    
    if item1.get('content') == item2.get('content'):
        print("  -> CONTENT MATCHES EXACTLY!")
    else:
        print("  -> Content has differences.")
