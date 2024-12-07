import os
import logging
from typing import List, Tuple
from langchain.docstore.document import Document
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Ensure the environment variables are correctly set
PG_VECTOR_DRIVER = os.getenv('PG_VECTOR_DRIVER')
PG_VECTOR_USER = os.getenv('PG_VECTOR_USER')
PG_VECTOR_PASSWORD = os.getenv('PG_VECTOR_PASSWORD')
PG_VECTOR_HOST = os.getenv('PG_VECTOR_HOST')
PG_VECTOR_PORT = os.getenv('PG_VECTOR_PORT')
PG_VECTOR_DATABASE_NAME = os.getenv('PG_VECTOR_DATABASE_NAME')

class TranscriptRepository:
    def __init__(self):
        # Construct the connection string
        self.CONNECTION_STRING = f"{PG_VECTOR_DRIVER}://{PG_VECTOR_USER}:{PG_VECTOR_PASSWORD}@{PG_VECTOR_HOST}:{PG_VECTOR_PORT}/{PG_VECTOR_DATABASE_NAME}"

    async def get_by_semantic_relevance_async(self, session_id: str, query: str, results_count: int = 1) -> List[Tuple[Document, float]]:        # TODO: async: asimilary_search
        # NOTE: I have tried making this async twice already and cannot figure it out. 
        return self._get_vector_store(session_id).max_marginal_relevance_search_with_score(query=query, float=0.5, k=results_count)
    
    async def save_resume_embeddings_async(self, documents: List[Document]) -> None:
        pg_vectorstore = self._get_vector_store("resume")
        pg_vectorstore.add_documents(documents)
        
        return
    
    async def delete_resume_embeddings_async(self) -> None:
        pg_vectorstore = self._get_vector_store("resume")
        pg_vectorstore.delete_collection()

        return
    
    # TODO: This removed self.vectorstore that would be common across all other functions. Right now, this
    # Langchain Managed PGVector connection
    def _get_vector_store(self, session_id: str):
        open_ai_embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=os.getenv("OPENAI_KEY"))
        
        # LANGCHAIN CONNECTION
        return PGVector(
            embeddings=open_ai_embeddings,
            collection_name=session_id,
            connection=self.CONNECTION_STRING,
            use_jsonb=True,
        )
    
    # Currently a DEBUG Function.
    def drop_all_embeddings(self, session_id, str) -> bool:
        try:
            self._get_vector_store(session_id).drop_tables()
            logging.info("Successfully dropped all embeddings.")
            return True
        except Exception as e:
            logging.error(f"Failed to drop embeddings: {str(e)}")
            return False