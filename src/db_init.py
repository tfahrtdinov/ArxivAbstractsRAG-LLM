import logging
from typing import Iterable, List

import pyarrow.parquet as pq
from langchain_core.documents import Document

from src.dependencies import get_vectorstore


logger = logging.getLogger(__name__)

# NOTE: This file isn't supposed to be a part of an app. For the fastapi with llm, I'm assuming you already have vectors in DB
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
    store = get_vectorstore()
    for docs in documents_generator(parquet_file):
        store.add_documents(docs, ids=[doc.id for doc in docs])

    logger.info("Documents encoded")


if __name__ == "__main__":
    encode_docs()
