from functools import lru_cache

from dotenv import load_dotenv
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain.schema import BaseRetriever

from src.rag_service.rag_service import RAGService
from src.settings.settings import Settings


load_dotenv()


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore


@lru_cache(maxsize=1)
def get_retriver() -> BaseRetriever:
    settings = get_settings()
    vectorstore = PGVector(
        connection=settings.POSTGRES_CONNECTOR,
        collection_name=settings.VECTOR_STORE_COLLECTION_NAME,
        embeddings=OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL
        ),
    )
    return vectorstore.as_retriever(search_kwargs={"k": 5})


@lru_cache(maxsize=1)
def get_rag_service() -> RAGService:
    return RAGService(retriever=get_retriver(), settings=get_settings())
