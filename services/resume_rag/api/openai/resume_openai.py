import os
from openai import OpenAI
from typing import List
from langchain.docstore.document import Document
from services.resume_rag.api.openai.models.resume_model import ResumeModel
from services.resume_rag.api.services.models.resume_inference_model import ResumeInferenceModel

class ResumeOpenAI:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_KEY'))
    
    async def parse_resume_async(self, text: str, n_descriptions: int = 13) -> ResumeModel:        
        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": f"Extract the resume information. In this resume, there are {n_descriptions} bulletpoints describing work experience."},
                {"role": "user", "content": text},
            ],
            response_format=ResumeModel
        )
        
        return completion.choices[0].message.parsed
    
    async def extend_user_query_async(self, query: str) -> str:
        completion = self.client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "Convert the following user query into a chunk of text comparable to what can be found on bullet points on a resume. The raw output will be converted to an embedding for cosine-similar searches. Leave names out of it and enrich in technical keywords and semantic meaning."},
                {"role": "user", "content": query},
            ]
        )
        
        return completion.choices[0].message.content
        
    async def get_resume_inference_async(self, query, documents: List[Document]):        
        context = "Below is a list of context sources. What ever is mentioned MUST be included in context sources to trace back the source of the info:"
        for doc in documents:
            # Temporarily append "At <Company Name>: <Bullet Point>" for LLM Context
            context += f'At {doc.metadata.get("company", "Experience")}: {doc.metadata.get("source_text", "Work Description")}\n'
        
        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "You are an interactive chat interface answering questions regarding the resume of Timothy Villaraza. Provide both the llm response and context sources that were used in the response. The response must brief at 50 - 80 words max."},
                {"role": "user", "content": context},
                {"role": "user", "content": query},
            ],
            response_format=ResumeInferenceModel
        )
        
        # Remove "At <Company Name>: <Bullet Point>"
        llm_response = completion.choices[0].message.parsed
        for i, source in enumerate(llm_response.context_sources):
            llm_response.context_sources[i] = source.split(": ", maxsplit=1)[1] if ": " in source else source
        
        return llm_response