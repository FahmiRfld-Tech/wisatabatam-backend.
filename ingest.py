"""Build the sample RAG index without deleting an existing database."""
import hashlib
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend_pariwisata.settings")


def main():
    import django
    django.setup()

    from django.conf import settings
    from langchain_core.documents import Document
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from api.services.retrieval import get_vectorstore

    source = settings.BASE_DIR / "data_wisata" / "info_wisata.txt"
    text = source.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError("Sample corpus is empty.")
    document = Document(page_content=text, metadata={"source": "data_wisata/info_wisata.txt"})
    chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents([document])
    ids = [hashlib.sha256(f"{i}:{doc.page_content}".encode("utf-8")).hexdigest()
           for i, doc in enumerate(chunks)]
    store = get_vectorstore(settings.RAG_STORE_PATH, settings.RAG_COLLECTION)
    store.add_documents(chunks, ids=ids)
    print(f"Indexed {len(chunks)} sample chunks. Repeated unchanged input uses the same IDs.")


if __name__ == "__main__":
    main()
