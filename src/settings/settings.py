from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
    POSTGRES_HOST: str
    POSTGRES_CONNECTOR: str
    VECTOR_STORE_COLLECTION_NAME: str

    OPENAI_API_KEY: str
    EMBEDDING_MODEL: str
    RETRIEVER_MODEL: str
    MAIN_MODEL: str
