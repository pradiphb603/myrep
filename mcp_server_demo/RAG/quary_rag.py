from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

VECTOR_DB_DIR = "../chroma_db"

# Initialize embeddings
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# Load existing vector database
vector_db = Chroma(
    collection_name="eda_documents",
    embedding_function=embeddings,
    persist_directory=VECTOR_DB_DIR
)

# Initialize LLM
llm = OllamaLLM(
    model="beam:cloud",
    temperature=0
)

# Create retriever
retriever = vector_db.as_retriever(
    search_kwargs={"k": 4}
)

# Prompt template
prompt = ChatPromptTemplate.from_template("""
Answer the question using the following context.

Context:
{context}

Question:
{question}

If the answer is not available in the context,
say that you cannot find the answer in the documents.
""")


def ask_question(question):
    # Retrieve relevant documents
    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    # Generate answer
    chain = prompt | llm

    response = chain.invoke({
        "context": context,
        "question": question
    })

    print("\nAnswer:")
    print(response)

    print("\nSources:")

    for doc in docs:
        print(doc.metadata.get("source"))


if __name__ == "__main__":

    while True:

        question = input("\nEnter question (exit to quit): ")

        if question.lower() == "exit":
            break

        ask_question(question)