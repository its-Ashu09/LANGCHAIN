import json

file_path = r'c:\Users\ashut\OneDrive\Desktop\Intern\INTERNSHIP\jsonData\cgl_11_09_2024_shift_1_tier1.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 1. Analyze Collision for 630680412338
print("--- COLLISION ANALYSIS: 630680412338 ---")
colliding_items = [q for q in data if str(q.get('qID')) == "630680412338"]
for i, item in enumerate(colliding_items):
    print(f"\nItem {i+1}:")
    print(f"  Subject: {item.get('meta', {}).get('subject')}")
    print(f"  Question: {item.get('content', {}).get('question_text', {}).get('en')[:150]}...")

# 2. Analyze Invalid Lengths
print("\n--- INVALID LENGTH ANALYSIS ---")
invalid_qids = [q for q in data if len(str(q.get('qID'))) != 12]
print(f"\nQuestions with Invalid qID Length ({len(invalid_qids)}):")
for q in invalid_qids:
    print(f"  qID: {q.get('qID')} (Len: {len(str(q.get('qID')))})")
    print(f"    Subject: {q.get('meta', {}).get('subject')}")
    print(f"    Text: {q.get('content', {}).get('question_text', {}).get('en')[:50]}...")

# Sample Invalid Option IDs
print(f"\nSample Invalid Option IDs (First 5):")
count = 0
for q in data:
    qid = q.get('qID')
    for opt in q.get('options', []):
        oid = str(opt.get('id'))
        if len(oid) != 13:
            print(f"  Q:{qid} -> Opt:{oid} (Len: {len(oid)})")
            count += 1
            if count >= 5: break
    if count >= 5: break
