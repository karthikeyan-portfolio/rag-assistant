import os
from dotenv import load_dotenv

from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)
from langchain_core.prompts import PromptTemplate


load_dotenv()

INDEX_NAME = "document-rag-store"


def get_vectorstore():

    google_api_key = os.getenv("GOOGLE_API_KEY")
    pinecone_api_key = os.getenv("PINECONE_API_KEY")

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


def retrieve_context(query: str, k: int = 4):

    vectorstore = get_vectorstore()

    docs = vectorstore.similarity_search(query, k=k)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    return context


def generate_response(query: str):

    google_api_key = os.getenv("GOOGLE_API_KEY")

    context = retrieve_context(query)

    prompt = """
    You are a helpful AI assistant.

    Answer the user question using ONLY the retrieved context.

    If the answer is not available in the context,
    say "I don't know based on the provided documents."

    User Question:
    {query}

    Retrieved Context:
    {context}
    """

    prompt_template = PromptTemplate.from_template(prompt)

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=google_api_key
    )

    chain = prompt_template | llm

    response = chain.invoke({
        "query": query,
        "context": context
    })

    return response.content