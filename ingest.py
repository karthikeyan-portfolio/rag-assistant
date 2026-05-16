import os
import re
import hashlib
from dotenv import load_dotenv

from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()

INDEX_NAME = "document-rag-store"

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()


def hash_text(text: str) -> str:
    return hashlib.sha256(normalize(text).encode()).hexdigest()


def load_document(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    loader = UnstructuredWordDocumentLoader(file_path)
    return loader.load()


def get_vectorstore():
    google_api_key = os.getenv("GOOGLE_API_KEY")
    pinecone_api_key = os.getenv("PINECONE_API_KEY")

    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY not found")

    if not pinecone_api_key:
        raise ValueError("PINECONE_API_KEY not found")

    pc = Pinecone(api_key=pinecone_api_key)
    index = pc.Index(INDEX_NAME)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-2-preview",
        google_api_key=google_api_key
    )

    vectorstore = PineconeVectorStore(
        index=index,
        embedding=embeddings
    )

    return vectorstore


def ingest_documents(file_path: str):

    docs = load_document(file_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " "]
    )

    chunks = splitter.split_documents(docs)

    vectorstore = get_vectorstore()

    batch_docs = []
    batch_ids = []

    for chunk in chunks:

        chunk_hash = hash_text(chunk.page_content)

        chunk.metadata["source"] = os.path.basename(file_path)
        chunk.metadata["hash"] = chunk_hash

        batch_docs.append(chunk)
        batch_ids.append(chunk_hash)

        if len(batch_docs) >= 100:
            vectorstore.add_documents(
                documents=batch_docs,
                ids=batch_ids
            )

            batch_docs.clear()
            batch_ids.clear()

    if batch_docs:
        vectorstore.add_documents(
            documents=batch_docs,
            ids=batch_ids
        )

    print("Documents ingested successfully!")

if __name__ == "__main__":
    file_path = "SmartCare Hospital.docx"
    ingest_documents(file_path)