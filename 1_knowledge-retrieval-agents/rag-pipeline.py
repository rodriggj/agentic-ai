import argparse
import os
import sys
from typing import List

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PDFMinerLoader
from langchain_classic.chains import RetrievalQA

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"), override=True)
# Disable LangChain tracing telemetry by default when a LangSmith key is not configured.
os.environ["LANGCHAIN_TRACING_V2"] = "false"

OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4-turbo")
OPENAI_EMBEDDING_MODEL = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")

parser = argparse.ArgumentParser(description="Run the RAG pipeline and report progress.")
parser.add_argument("--docs-path", default="./docs", help="Path to the document directory")
parser.add_argument("--query", "-q", required=True, help="Question to ask the retrieval pipeline")
parser.add_argument("--verbose", action="store_true", help="Print detailed progress output")
# `args` will be populated in `main()` to avoid parsing CLI args at import time (so unit tests can import helpers).
args = None


def log(msg: str) -> None:
    print(msg)


def debug(msg: str) -> None:
    # Safe check for verbose flag even when `args` is not set (e.g. during unit tests import).
    if getattr(args, "verbose", False):
        print(msg)


def validate_docs_path(path: str) -> None:
    if not os.path.isdir(path):
        raise FileNotFoundError(f"Documents path does not exist: {path}")


def load_documents(path: str) -> List:
    """Load PDF and text documents from disk with basic error handling."""
    docs = []
    # PDF loader may fail on malformed PDFs; capture its errors separately.
    try:
        pdf_loader = DirectoryLoader(path, glob="*.pdf", loader_cls=PDFMinerLoader)
        try:
            docs += pdf_loader.load()
        except Exception as e:
            debug(f"PDF loader error: {e}")
    except Exception as e:
        debug(f"Could not initialize PDF loader: {e}")

    try:
        text_loader = DirectoryLoader(path, glob="*.txt")
        try:
            docs += text_loader.load()
        except Exception as e:
            debug(f"Text loader error: {e}")
    except Exception as e:
        debug(f"Could not initialize text loader: {e}")

    return docs


def split_into_chunks(documents: List):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)
    if not chunks:
        raise RuntimeError("No chunks created from documents")
    return chunks


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10), retry=retry_if_exception_type(Exception))
def build_vectorstore_with_retries(chunks):
    debug("Creating embeddings (may be retried on transient failure)")
    embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)
    vs = FAISS.from_documents(chunks, embeddings)
    return vs


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8), retry=retry_if_exception_type(Exception))
def run_query_with_retries(chain, query: str):
    debug("Invoking QA chain (with retries)")
    return chain.invoke({"query": query})


def main() -> int:
    try:
        # Parse CLI args here so module import doesn't trigger argparse parsing.
        global args
        args = parser.parse_args()

        # Step 1: Validate and notify about API key
        log("STEP 1/6: Validating configuration and environment")
        validate_docs_path(args.docs_path)
        if not os.environ.get("OPENAI_API_KEY"):
            log("OPENAI_API_KEY not set in environment; ensure it is configured before running")
            raise EnvironmentError("OPENAI_API_KEY is required")

        # Step 2: Load documents
        log(f"STEP 2/6: Loading documents from {args.docs_path}")
        documents = load_documents(args.docs_path)
        if not documents:
            raise ValueError(f"No documents were loaded from {args.docs_path}. Make sure PDF or TXT files exist in that folder.")

        # Step 3: Split
        log("STEP 3/6: Splitting documents into chunks")
        chunks = split_into_chunks(documents)
        log(f"  Loaded {len(documents)} documents and created {len(chunks)} chunks")

        # Step 4: Embeddings + FAISS with retries
        log("STEP 4/6: Creating embeddings and building FAISS index")
        vectorstore = build_vectorstore_with_retries(chunks)

        # Step 5: Retriever + QA chain
        log("STEP 5/6: Defining retriever and QA chain")
        log(f"Using OpenAI model: {OPENAI_MODEL}")
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0)
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            return_source_documents=True,
        )

        # Step 6: Run query with retries
        log("STEP 6/6: Running the query")
        result = run_query_with_retries(qa_chain, args.query)

        if not isinstance(result, dict) or "result" not in result:
            raise RuntimeError("Unexpected response shape from the QA chain")

        print("Answer:", result.get("result"))
        print("\nSources:")
        for doc in result.get("source_documents", []):
            print("-", doc.metadata.get("source", "unknown"))

        return 0
    except Exception as exc:
        print("Error during RAG pipeline execution:", str(exc))
        debug(getattr(exc, "__traceback__", "No traceback available"))
        return 1


if __name__ == "__main__":
    sys.exit(main())
