from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class TextPair(BaseModel):
    en: str
    hi: str

class OptionText(BaseModel):
    id: str
    text: TextPair

class QuestionContent(BaseModel):
    question_text: TextPair
    passage_text: Optional[TextPair] = Field(default=None, description="Include FULL passage if comprehension based")
    is_image_based: bool

class MetaData(BaseModel):
    exam_name: str = "CGL"
    year: int = 2024
    tier: str = "Tier1"
    subject: str
    topic: str = "Unknown"
    sub_topic: str = "Unknown"
    difficulty: str = "Medium"
    languages: List[str] = ["en", "hi"]
    date: str
    shift: str

class AnswerKey(BaseModel):
    correct_option_id: str
    solution_text: TextPair

class Question(BaseModel):
    id: str = Field(description="Random UUID")
    qID: str = Field(description="Question ID from PDF")
    meta: MetaData
    content: QuestionContent
    options: List[OptionText]
    answer: AnswerKey

# Batch Container
class QuestionBatch(BaseModel):
    questions: List[Question]