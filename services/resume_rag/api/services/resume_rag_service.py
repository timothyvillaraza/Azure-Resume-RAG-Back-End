import logging
import requests
from bs4 import BeautifulSoup, Comment
from langchain.docstore.document import Document

# Repositories
from services.resume_rag.api.repositories.transcript_repository import TranscriptRepository
# Chains
from services.resume_rag.api.openai.resume_openai import ResumeOpenAI
# Models
from services.resume_rag.api.services.models.resume_inference_model import ResumeInferenceModel

class ResumeRagService:
    def __init__(self):
        self._transcriptRepository = TranscriptRepository()
    
    async def get_resume_inference_async(self, query: str) -> ResumeInferenceModel:
        # Get Relevant Documents from Repository
        retrieved_documents_score_tuples = await self._transcriptRepository.get_by_semantic_relevance_async(session_id='resume', query=query, results_count=50)
        
        # TODO: Optimize retrieval by cleaning up embedded document sources, removing timestamps from chunks,
        #       adding heuristics, or using a different embedding model.

        # Example improvement: Filter documents by score > 0.8
        retrieved_documents = [document for document, score in retrieved_documents_score_tuples]
        
        # Save user message, get LLM response, save LLM response 
        resume_openai = ResumeOpenAI()
        llm_response = await resume_openai.get_resume_inference_async(query, retrieved_documents)
        
        return llm_response
    
    async def save_resume_embeddings_from_iframe(self, url: str) -> None:
        iframe_content = requests.get(url)
        
        if iframe_content.status_code == 200:
            iframe_html_content = iframe_content.text

            soup = BeautifulSoup(iframe_html_content, 'lxml')

            resume_texts = _extract_all_text(soup)
            
            documents = [Document(page_content=text) for text in resume_texts]
            
            await self._transcriptRepository.save_resume_embeddings(documents)
        else:
            print(f"Failed to retrieve content from {url}")
        
        return
      
    async def delete_resume_embeddings(self) -> None:
        await self._transcriptRepository.delete_resume_embeddings()
        return
        

# =======================================
# Helper Functions
# =======================================
def _extract_all_text(soup) -> set[str]:
    all_text_elements = set()

    for element in soup.find_all(text=True):
        # Exclude text from script, style, and similar non-visible elements
        if element.parent.name not in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            # Exclude comments and non-visible elements
            if not isinstance(element, Comment):
                text = element.strip()  # Remove leading/trailing whitespace
                if text and not element.isspace() and len(text) > 1:  # Only add non-empty strings and skip whitespace
                    all_text_elements.add(text)

    return all_text_elements