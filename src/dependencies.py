from functools import lru_cache

from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain.schema import BaseRetriever
from langchain_community.utilities import SQLDatabase

from src.rag_service.rag_service import RAGService
from src.settings.settings import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore


@lru_cache()
def get_db_size() -> int:
    settings = get_settings()
    db = SQLDatabase.from_uri(settings.POSTGRES_CONNECTOR.format(HOST=settings.POSTGRES_HOST))
    return int(db.run("SELECT COUNT(*) FROM langchain_pg_embedding;").strip("[](), "))


@lru_cache
def get_vectorstore() -> PGVector:
    settings = get_settings()

    vectorstore = PGVector(
        connection=settings.POSTGRES_CONNECTOR.format(HOST=settings.POSTGRES_HOST),
        collection_name=settings.VECTOR_STORE_COLLECTION_NAME,
        embeddings=OpenAIEmbeddings(model=settings.EMBEDDING_MODEL),
    )
    return vectorstore


@lru_cache(maxsize=1)
def get_retriver() -> BaseRetriever:
    return get_vectorstore().as_retriever(search_kwargs={"k": 5})


@lru_cache(maxsize=1)
def get_rag_service() -> RAGService:
    return RAGService(retriever=get_retriver(), settings=get_settings())
