# from fastapi import FastAPI
# from pydantic import BaseModel
# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv
# import os

# # Step 1: Load environment variables (.env file)
# load_dotenv()
# api_key = os.getenv("GOOGLE_API_KEY")

# # Step 2: Initialize Gemini model
# model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# # Step 3: Create FastAPI app
# app = FastAPI()

# # Step 4: Define message schema
# class Message(BaseModel):
#     user_input: str

# # Step 5: Create POST endpoint
# @app.post("/chat")
# def chat(message: Message):
#     response = model.invoke(message.user_input)
#     return {"bot_reply": response.content}


from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Generative AI Career Roadmap (Final PDF)', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, 'Fast Career | Less Math | Industry Ready', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        # Light blue background fill
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 7, body)
        self.ln()

def create_pdf():
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Content Structure - REPLACED BULLETS WITH DASHES (-) TO FIX ERROR
    content = [
        ("Target Roles", 
         "- AI Application Engineer\n- LLM Engineer\n- GenAI Developer\n- Backend + AI Engineer"),
        
        ("Prerequisites", 
         "- Python\n- FastAPI\n- LangChain\n- Databases"),
        
        ("Career Flow Overview", 
         "LLM Basics -> Prompting -> RAG -> Agents -> Production -> Deployment -> Job\n\nTotal Time: 4-6 Months"),
        
        ("1. LLM Fundamentals (2-3 Weeks)", 
         "LEARN:\n- What is LLM (high-level), Tokens, context window\n- Temperature, top-p, Hallucinations\n- System vs User prompts\n- NO math, NO model training\n\nYouTube Resources:\n- Jay Alammar - How LLMs Work\n- Fireship - LLM Explained\n- freeCodeCamp - LLMs for Developers\n\nPRACTICE:\n- Basic chatbot\n- JSON output control"),
        
        ("2. Prompt Engineering (2 Weeks)", 
         "LEARN:\n- Zero-shot / Few-shot\n- Role prompting, Output schemas\n- Prompt templates, Guardrails\n\nYouTube Resources:\n- freeCodeCamp - Prompt Engineering Full Course\n- DeepLearning.AI - Prompt Engineering\n- CodeWithHarry (Hindi)\n\nPROJECTS:\n- Resume -> JSON\n- Text -> SQL\n- Email classifier"),
        
        ("3. Embeddings & Vector Databases (3 Weeks)", 
         "LEARN:\n- Embeddings, Semantic search\n- Chunking, Metadata filtering\n\nTOOLS:\n- FAISS | Chroma | Pinecone\n\nYouTube Resources:\n- Pinecone - Embeddings Explained\n- freeCodeCamp - Vector DB\n- Krish Naik - FAISS\n\nPROJECT:\n- PDF -> Embeddings -> Search"),
        
        ("4. RAG (Retrieval Augmented Generation) (3 Weeks)", 
         "LEARN:\n- RAG architecture\n- Context ranking, Query rewriting\n- Hallucination control\n\nYouTube Resources (MOST IMPORTANT):\n- Pinecone - RAG Explained\n- freeCodeCamp - RAG with LangChain\n- Krish Naik - PDF Chatbot\n\nPROJECTS:\n- Company docs chatbot\n- Legal / medical QA bot\n- Deployment mandatory"),
        
        ("5. Agents & Tool Calling (2-3 Weeks)", 
         "LEARN:\n- Function calling, Tool usage\n- Multi-step reasoning\n- LangGraph\n\nYouTube Resources:\n- LangChain Agents\n- Function Calling\n- LangGraph\n\nPROJECT:\n- AI agent (email -> web -> DB -> reply)"),
        
        ("6. Production Engineering (3 Weeks)", 
         "LEARN:\n- Async FastAPI, Docker\n- Celery + Redis\n- JWT Auth, Rate limiting, Logging\n\nYouTube Resources:\n- freeCodeCamp - FastAPI Advanced\n- TechWorld with Nana - Docker\n\nPROJECT:\n- Production-ready AI API"),
        
        ("7. Deployment & Cloud (2 Weeks)", 
         "LEARN:\n- AWS basics, Secrets management\n- CI/CD basics\n\nYouTube Resources:\n- FastAPI on AWS\n- Render Deployment\n- AWS Hindi - Apna College"),
        
        ("8. Portfolio & Job Prep (2 Weeks)", 
         "MUST-HAVE PROJECTS:\n- RAG chatbot\n- AI automation agent\n- LLM API service\n- Vector search system\n\nYouTube Resources:\n- GenAI Resume\n- AI Interview Prep\n\nSALARY REALITY:\n- Entry: 8-15 LPA\n- 2-3 Years: 20-35 LPA"),
        
        ("FINAL TRUTH", 
         "AI banana nahi -- AI ko production mein use karna hi career hai.")
    ]

    for title, body in content:
        pdf.chapter_title(title)
        pdf.chapter_body(body)

    pdf.output("GenAI_Career_Roadmap.pdf")
    print("PDF Generated Successfully: GenAI_Career_Roadmap.pdf")

if __name__ == "__main__":
    create_pdf()