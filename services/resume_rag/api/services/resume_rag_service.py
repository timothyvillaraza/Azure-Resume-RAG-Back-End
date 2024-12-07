import logging
import requests
from langchain.docstore.document import Document
from io import BytesIO
from PyPDF2 import PdfReader

# Repositories
from services.resume_rag.api.repositories.transcript_repository import TranscriptRepository
# Chains
from services.resume_rag.api.openai.resume_openai import ResumeOpenAI
# Models
from services.resume_rag.api.services.models.resume_inference_model import ResumeInferenceModel

class ResumeRagService:
    def __init__(self):
        self._resume_open_ai = ResumeOpenAI()
        self._transcriptRepository = TranscriptRepository()
    
    async def get_resume_inference_async(self, user_query: str) -> ResumeInferenceModel:
        # User Query -> AI Extended User Query
        ai_extended_query = await self._resume_open_ai.extend_user_query_async(user_query)
        
        # AI Extended User Query -> Relevant Resume Bullet Points
        retrieved_documents_score_tuples = await self._transcriptRepository.get_by_semantic_relevance_async(collection='resume', query=ai_extended_query, results_count=7)
        
        retrieved_documents = [document for document, score in retrieved_documents_score_tuples]
        
        # Send LLM User Query + Context
        llm_response = await self._resume_open_ai.get_resume_inference_async(user_query, retrieved_documents)
        
        return llm_response
    
    async def save_resume_embeddings_from_pdf(self, pdf: BytesIO) -> None:
        # PDF Resume -> Plain Text Resume
        resume_text = _extract_text_from_pdf(pdf)
        
        # Plain Text Resume -> Structured In-Memory Resume
        resume_model = await self._resume_open_ai.parse_resume_async(resume_text, n_descriptions=13)
        
        # Resume Bullet Points -> Langchain Documents
        documents = []
        for experience in resume_model.professional_experience: # Each company worked at
            for responsibility in experience.responsibilities:  # Each bullet point description                
                bullet_point_doc = Document(
                    page_content=responsibility.ai_extended_description, # Used in embedding generation
                    metadata={
                        "source_text": responsibility.description,
                        "skills": responsibility.skills,
                        "company": experience.company
                    }
                )
                
                documents.append(bullet_point_doc)
        
        # Langchain Documents -> Vector Embeddings
        await self._transcriptRepository.save_resume_embeddings_async(documents)
      
    async def delete_resume_embeddings(self) -> None:
        await self._transcriptRepository.delete_resume_embeddings_async()
        

# =======================================
# Helper Functions
# =======================================
def _extract_text_from_pdf(pdf: BytesIO) -> str:
    # Extracted Text
    resume_text = ""
    
    reader = PdfReader(pdf)  # Open the PDF reader directly

    # Extract text from all pages
    for page in reader.pages:
        resume_text += page.extract_text() or ""  # Handle NoneType safely

    return resume_text
