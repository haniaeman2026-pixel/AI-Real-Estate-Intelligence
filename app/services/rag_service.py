from pathlib import Path
import re

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DOCUMENTS_DIR = BASE_DIR / "documents"


# ============================================================
# RAG CONFIGURATION
# ============================================================

documents = []

vectorizer = None

document_matrix = None


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text: str):

    text = text.replace(
        "\x00",
        " "
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# CREATE CHUNKS
# ============================================================

def create_chunks(
    text: str,
    chunk_size: int = 900,
    overlap: int = 150,
):

    text = clean_text(text)

    if not text:
        return []

    chunks = []

    start = 0

    text_length = len(text)

    while start < text_length:

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():
            chunks.append(
                chunk.strip()
            )

        if end >= text_length:
            break

        start = end - overlap

    return chunks


# ============================================================
# LOAD DOCUMENTS
# ============================================================

def load_documents():

    global documents

    documents = []

    DOCUMENTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    files = list(
        DOCUMENTS_DIR.glob("*.txt")
    )

    for file_path in files:

        try:

            text = file_path.read_text(
                encoding="utf-8"
            )

            chunks = create_chunks(
                text
            )

            for index, chunk in enumerate(
                chunks
            ):

                documents.append(
                    {
                        "source": file_path.name,

                        "chunk_id": index,

                        "text": chunk,
                    }
                )

        except Exception as exc:

            print(
                f"Could not read "
                f"{file_path.name}: {exc}"
            )

    return documents


# ============================================================
# INITIALIZE RAG
# ============================================================

def initialize_rag():

    global vectorizer
    global document_matrix

    load_documents()

    if not documents:

        vectorizer = None

        document_matrix = None

        print(
            "No RAG documents found."
        )

        return

    texts = [
        document["text"]
        for document in documents
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=10000,
    )

    document_matrix = vectorizer.fit_transform(
        texts
    )

    print(
        f"RAG initialized with "
        f"{len(documents)} document chunks."
    )


# ============================================================
# STATUS
# ============================================================

def rag_status():

    return {
        "feature": "RAG Knowledge Assistant",

        "status": (
            "online"
            if document_matrix is not None
            else "offline"
        ),

        "documents": len(documents),

        "knowledge_directory": str(
            DOCUMENTS_DIR
        ),
    }


# ============================================================
# RETRIEVE DOCUMENTS
# ============================================================

def retrieve_documents(
    question: str,
    top_k: int = 3,
):

    if (
        vectorizer is None
        or document_matrix is None
        or not documents
    ):

        return []

    query_vector = vectorizer.transform(
        [question]
    )

    similarities = cosine_similarity(
        query_vector,
        document_matrix,
    )[0]

    ranked_indexes = (
        similarities.argsort()[::-1]
    )

    results = []

    for index in ranked_indexes[:top_k]:

        score = float(
            similarities[index]
        )

        if score <= 0:
            continue

        document = documents[index].copy()

        document["score"] = round(
            score,
            4,
        )

        results.append(
            document
        )

    return results


# ============================================================
# EXTRACT RELEVANT SENTENCES
# ============================================================

def extract_relevant_text(
    question: str,
    retrieved_documents: list,
):

    if not retrieved_documents:

        return ""

    question_words = set(
        re.findall(
            r"\b[a-zA-Z]{3,}\b",
            question.lower(),
        )
    )

    selected_parts = []

    for document in retrieved_documents:

        sentences = re.split(
            r"(?<=[.!?])\s+",
            document["text"],
        )

        scored_sentences = []

        for sentence in sentences:

            sentence_words = set(
                re.findall(
                    r"\b[a-zA-Z]{3,}\b",
                    sentence.lower(),
                )
            )

            overlap = len(
                question_words
                &
                sentence_words
            )

            scored_sentences.append(
                (
                    overlap,
                    sentence,
                )
            )

        scored_sentences.sort(
            reverse=True,
            key=lambda item: item[0],
        )

        best_sentences = [
            sentence
            for score, sentence
            in scored_sentences[:3]
            if score > 0
        ]

        if not best_sentences:

            best_sentences = [
                document["text"][:700]
            ]

        selected_parts.extend(
            best_sentences
        )

    return " ".join(
        selected_parts
    )


# ============================================================
# RAG ANSWER
# ============================================================

def answer_with_rag(question: str):

    retrieved = retrieve_documents(
        question,
        top_k=3,
    )

    if not retrieved:

        return {
            "success": True,

            "answer": (
                "I could not find relevant information "
                "in the uploaded real-estate knowledge "
                "documents."
            ),

            "sources": [],

            "retrieved_chunks": 0,
        }

    context = extract_relevant_text(
        question,
        retrieved,
    )

    answer = (
        "Based on the available knowledge documents:\n\n"
        + context
    )

    sources = []

    for document in retrieved:

        sources.append(
            {
                "source": document["source"],

                "chunk_id": document["chunk_id"],

                "similarity_score": document["score"],
            }
        )

    return {
        "success": True,

        "answer": answer,

        "sources": sources,

        "retrieved_chunks": len(
            retrieved
        ),

        "grounded": True,
    }