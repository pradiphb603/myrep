import os
import uuid
from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


# Configuration
DOCUMENT_DIR = "../documents"
VECTOR_DB_DIR = "../chroma_db"

COLLECTION_NAME = "eda_documents"

EMBEDDING_MODEL = "nomic-embed-text"


def load_documents(directory):

    documents = []

    directory = Path(directory)

    if not directory.exists():
        raise FileNotFoundError(
            f"Document directory not found: {directory}"
        )

    for file in directory.rglob("*"):

        if not file.is_file():
            continue

        try:
            print(f"Loading: {file}")

            if file.suffix.lower() == ".pdf":

                loader = PyPDFLoader(str(file))
                docs = loader.load()

            elif file.suffix.lower() in [".txt", ".md"]:

                loader = TextLoader(
                    str(file),
                    encoding="utf-8"
                )

                docs = loader.load()

            else:
                continue

            # Add source metadata
            for doc in docs:
                doc.metadata["source"] = str(file)
                doc.metadata["filename"] = file.name

            documents.extend(docs)

        except Exception as error:
            print(f"Error loading {file}: {error}")

    return documents


def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    chunks = splitter.split_documents(documents)

    print(f"Total document pages/files: {len(documents)}")
    print(f"Total chunks generated: {len(chunks)}")

    return chunks


def add_documents_to_vector_db(chunks):

    # Initialize embedding model
    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL,
        base_url="http://localhost:11434"
    )

    # Connect to persistent ChromaDB
    vector_db = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=VECTOR_DB_DIR
    )

    # Generate unique IDs for chunks
    ids = [str(uuid.uuid4()) for _ in chunks]

    # Add documents
    vector_db.add_documents(
        documents=chunks,
        ids=ids
    )

    print("Documents successfully added to ChromaDB!")

    return vector_db


def main():

    # Step 1: Load documents
    documents = load_documents(DOCUMENT_DIR)

    if not documents:
        print("No supported documents found.")
        return

    # Step 2: Split documents
    chunks = split_documents(documents)

    # Step 3: Add to vector database
    add_documents_to_vector_db(chunks)


if __name__ == "__main__":
    main()