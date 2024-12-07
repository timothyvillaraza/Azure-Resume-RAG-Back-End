import os
import logging
from typing import List, Tuple
from langchain.docstore.document import Document
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from sqlalchemy import create_engine

# Ensure the environment variables are correctly set
PG_VECTOR_DRIVER = os.getenv('PG_VECTOR_DRIVER')
PG_VECTOR_USER = os.getenv('PG_VECTOR_USER')
PG_VECTOR_PASSWORD = os.getenv('PG_VECTOR_PASSWORD')
PG_VECTOR_HOST = os.getenv('PG_VECTOR_HOST')
PG_VECTOR_PORT = os.getenv('PG_VECTOR_PORT')
PG_VECTOR_DATABASE_NAME = os.getenv('PG_VECTOR_DATABASE_NAME')

class TranscriptRepository:
    def __init__(self):
        self.CONNECTION_STRING = f"{PG_VECTOR_DRIVER}://{PG_VECTOR_USER}:{PG_VECTOR_PASSWORD}@{PG_VECTOR_HOST}:{PG_VECTOR_PORT}/{PG_VECTOR_DATABASE_NAME}"
    
    async def get_by_semantic_relevance_async(self, collection: str, query: str, results_count: int = 5) -> List[Tuple[Document, float]]:        # TODO: async: asimilary_search
        return self._get_vector_store(collection).max_marginal_relevance_search_with_score(query=query, float=0.5, k=results_count)
    
    async def save_resume_embeddings_async(self, documents: List[Document]) -> None:
        self._get_vector_store("resume").add_documents(documents)
    
    async def delete_resume_embeddings_async(self) -> None:
        self._get_vector_store("resume").delete_collection()
    
    # NOTE: I have tried making this async twice already and cannot figure it out. 
    # Langchain Managed PGVector connection, needed if multiple collections are needed
    def _get_vector_store(self, collection: str) -> PGVector:
        open_ai_embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=os.getenv("OPENAI_KEY"))
        
        # LANGCHAIN CONNECTION
        return PGVector(
            embeddings=open_ai_embeddings,
            collection_name=collection,
            connection=self.CONNECTION_STRING,
            use_jsonb=True,
        )
    
    # DEBUG Function.
    # def drop_all_embeddings_async(self, session_id, str) -> None:
    #     self._get_vector_store(session_id).drop_tables()
