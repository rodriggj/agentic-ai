Reading the current rag-pipeline.py so I can explain exactly where FAISS is created and how chunks are stored.

Read [](file:///Users/gabrrodriguez/Desktop/agentic-ai/1_knowledge-retrieval-agents/rag-pipeline.py)

## Where FAISS is created

In rag-pipeline.py, the FAISS vector store is created here:

```python
vectorstore = build_vectorstore_with_retries(chunks)
```

and inside that helper:

```python
vs = FAISS.from_documents(chunks, embeddings)
```

So:
- `FAISS` is instantiated in memory
- it is created from the `chunks` list
- the actual embedding + vector index build happens inside `FAISS.from_documents(...)`

## Is it local?

Yes — it is locally instantiated in the running Python process.

This script does not currently save the FAISS index to disk, so:
- it exists only while the program runs
- once the script exits, that index is gone
- it is not a separate service or database server

## How are chunks written into it?

The `chunks` are a list of LangChain `Document` objects produced by:

```python
chunks = split_into_chunks(documents)
```

Then `FAISS.from_documents(chunks, embeddings)` does two things:
1. creates embeddings for each chunk using `OpenAIEmbeddings`
2. stores those vectors in the FAISS index
3. also keeps the chunk metadata/text in the FAISS docstore so retrieval can return sources

So the “write” step is internal to `FAISS.from_documents(...)`.

## How can you see the chunks?

The easiest way is to inspect `chunks` before FAISS is built:

```python
for i, chunk in enumerate(chunks[:10]):
    print(i, chunk.metadata)
    print(chunk.page_content[:400])
    print("---")
```

If you want to inspect the index object after creation, you can do something like:

```python
print("size:", vectorstore.index.ntotal)
print("docstore keys:", len(vectorstore.docstore._dict))
```

and if the docstore is accessible:

```python
for key, doc in list(vectorstore.docstore._dict.items())[:5]:
    print(key, doc.page_content[:200])
```

> Note: exact internals may differ by LangChain version, but the important part is that the chunks themselves come from `split_into_chunks(...)` and FAISS stores them in memory via `FAISS.from_documents(...)`.

## Summary

- `FAISS` is created in `build_vectorstore_with_retries()`
- it is local/in-memory
- chunks are written by `FAISS.from_documents(chunks, embeddings)`
- to inspect chunks, print the `chunks` list directly or inspect `vectorstore.docstore` after creation

If you want, I can also show you a small code snippet to add to rag-pipeline.py so it prints the first few chunks after splitting.