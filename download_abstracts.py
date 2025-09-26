import logging
from datasets import load_dataset

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ABSTRACT_DATASET = "gfissore/arxiv-abstracts-2021"
PARQUET_FILE_PATH = "data/abstracts.parquet"


def download_abstracts():
    logger.info("Downloading abstracts...")
    ds = load_dataset(ABSTRACT_DATASET)
    logger.info("Abstracts downloaded")
    ds["train"].select(range(20_000)).to_parquet(PARQUET_FILE_PATH)


if __name__ == "__main__":
    download_abstracts()
