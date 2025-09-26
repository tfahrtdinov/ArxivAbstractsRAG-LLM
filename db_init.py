import os
import logging
from typing import Iterable, List

import pyarrow.parquet as pq
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings

from download_abstracts import PARQUET_FILE_PATH


load_dotenv(".env")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# NOTE: This file isn't supposed to be a part of a fastapi app. I'm assuming you already have vectors in DB, before using RAG
EMBEDDING_MODEL = "text-embedding-3-small"


def documents_generator(parq_file: pq.ParquetFile) -> Iterable[List[Document]]:
    schema_pf = parq_file.schema_arrow
    metadata_columns = set(schema_pf.names) - {"title", "abstract", "categories"}

    for batch in parq_file.iter_batches(batch_size=4096):
        yield [
            Document(
                page_content=f"Title: {single_element['title']}\nAbstract: {single_element['abstract']}\nCategories:{' '.join(single_element['categories'])}",
                metadata={key: single_element[key] for key in metadata_columns},
            )
            for single_element in batch.to_pylist()
        ]


def split_documents(document: Iterable[Document]) -> None:
    # todo: implement later if document will get bigger
    pass


def encode_docs() -> None:
    parquet_file = pq.ParquetFile(PARQUET_FILE_PATH)

    store = PGVector(
        connection=os.getenv("POSTGRES_CONNECTOR").format(
            HOST=os.getenv("POSTGRES_HOST")
        ),
        collection_name=os.getenv("VECTOR_STORE_COLLECTION_NAME"),
        embeddings=OpenAIEmbeddings(model=EMBEDDING_MODEL),
    )
    logger.info("PGVector created")

    for docs in documents_generator(parquet_file):
        store.add_documents(docs, ids=[doc.id for doc in docs])

    logger.info("Documents encoded")


if __name__ == "__main__":
    encode_docs()
