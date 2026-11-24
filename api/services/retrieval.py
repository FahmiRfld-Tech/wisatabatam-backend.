"""Shared vector-store configuration for ingestion and chat."""
import logging
from functools import lru_cache

from django.conf import settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_vectorstore(path, collection):
    from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
    from langchain_community.vectorstores import Chroma

    return Chroma(collection_name=collection, persist_directory=str(path),
                  embedding_function=FastEmbedEmbeddings())


def retrieve(message):
    if not settings.RAG_STORE_PATH.is_dir():
        return "", []
    try:
        store = get_vectorstore(settings.RAG_STORE_PATH, settings.RAG_COLLECTION)
        docs = store.similarity_search(message, k=3)
    except Exception as exc:
        logger.warning("Retrieval unavailable (%s)", type(exc).__name__)
        return "", []
    context = "\n".join(doc.page_content[:2000] for doc in docs)
    sources = list(dict.fromkeys(
        doc.metadata["source"] for doc in docs if doc.metadata.get("source")
    ))
    return context, sources
