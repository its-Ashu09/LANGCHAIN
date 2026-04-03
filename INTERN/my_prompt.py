USER_PROMPT = """
IMPORTANT:
- Output MUST be a single JSON object
- Do NOT wrap JSON in ```json ``` or ``` ```
- Do NOT include any explanation text
- JSON must start with {{ and end with }}
- Use double quotes only
- numbers of question present in give PDF is must equal to total number of Qid or uuid.
- strictly prohibted to generate question by own.

CRITICAL RULE:
- Generate output ONLY if the input question is a complete exam question.
- DO NOT generate questions on your own and not create any question by link.
- DO NOT rephrase or split the question.
- If the input text is incomplete or http link based or instructional, return INVALID.

You are an expert SSC CGL exam question parser and content classifier.

Your task is to convert ONE exam question into a JSON object that STRICTLY follows the given schema.

NON-NEGOTIABLE RULES:
1. Output ONLY valid JSON
2. Do NOT add extra keys
3. Do NOT remove or rename keys
4. Follow the schema structure EXACTLY

FIXED META VALUES (DO NOT CHANGE):
- exam_name: "CGL"
- year: 2024
- tier: "Tier1"
- date: "09/09/2024"
- shift: "Morning Shift (9:00 AM – 10:00 AM)"
- languages: ["en","hi"]

INTELLIGENCE REQUIREMENTS:
- Decide subject, topic, sub_topic using SSC CGL syllabus
- Decide difficulty as Easy / Moderate / Hard
- Recognize mathematics topics like Trigonometry, Algebra, Arithmetic
- Recognize comprehension-based questions correctly
- Use is_image flag strictly; never guess image presence

SCHEMA:
{schema}

QUESTION:
{question}

IS IMAGE BASED:
{is_image}
"""
