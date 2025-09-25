import logging
from typing import Iterable, List
from dotenv import load_dotenv

import pyarrow.parquet as pq
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

from src.dependencies import get_settings


# todo: remove dotenv, add whole-app logger
load_dotenv()
logger = logging.getLogger(__name__)


# todo: это будет в докере, нужно будет указать путь относительно докера
PARQUET_FILE_PATH = "../data/abstracts.parquet"


def documents_generator(parq_file: pq.ParquetFile) -> Iterable[List[Document]]:
    schema_pf = parq_file.schema_arrow
    metadata_columns = set(schema_pf.names) - {"title", "abstract", "categories"}

    for batch in parq_file.iter_batches(batch_size=1024):
        yield [
            Document(
                page_content=f"Title: {single_element['title']}\nAbstract: {single_element['abstract']}\nCategories:{' '.join(single_element['categories'])}",
                metadata={key: single_element[key] for key in metadata_columns},
            )
            for single_element in batch.to_pylist()
        ]


def split_documents(document: Iterable[Document]) -> None:
    # todo: implement later when document will get bigger
    pass


def encode_docs() -> None:
    parquet_file = pq.ParquetFile(PARQUET_FILE_PATH)
    settings = get_settings()
    store = PGVector(
        connection=settings.POSTGRES_CONNECTOR,
        collection_name=settings.VECTOR_STORE_COLLECTION_NAME,
        embeddings=OpenAIEmbeddings(model=settings.EMBEDDING_MODEL),
    )
    for docs in documents_generator(parquet_file):
        store.add_documents(docs, ids=[doc.id for doc in docs])

    logger.info("Documents encoded")


if __name__ == "__main__":
    encode_docs()
