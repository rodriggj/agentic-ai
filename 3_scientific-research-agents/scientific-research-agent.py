# Quick implementation Example: Scientific Research Agent
# Phases: scan literature, -> cluster themes -> syntesize insights

# pip install arxiv sentence-transformers scikit-learn pandas numpy nltk

import os
import re
import time
import arxiv
import numpy as np
import pandas as pd
from collections import Counter
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

# --------------

# 1) Broad Literature Scanning

# ---------------
QUERY = "COBOL blocks and pre-compiled headers"  # Example query - change to your research topic
MAX_RESULTS = 80   # Keep small for demo purposes
CLUSTERS = 4       # tune to topic breadth

def search_arxiv(query, max_results=MAX_RESULTS, max_attempts=5):
    # num_retries=0 disables library-level retries so our backoff loop controls all retry logic
    client = arxiv.Client(page_size=20, delay_seconds=5, num_retries=0)
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    for attempt in range(max_attempts):
        try:
            results = []
            for r in client.results(search):
                results.append({
                    "title": r.title.strip(),
                    "summary": r.summary.strip(),
                    "authors": ", ".join(a.name for a in r.authors),
                    "published": r.published.strftime("%Y-%m-%d"),
                    "url": r.entry_id
                })
            return pd.DataFrame(results)
        except arxiv.HTTPError as e:
            if e.status in (429, 503) and attempt < max_attempts - 1:
                wait = 60 * (2 ** attempt)  # 60s, 120s, 240s, 480s
                print(f"HTTP {e.status}. Waiting {wait}s before retry {attempt + 1}/{max_attempts - 1}...")
                time.sleep(wait)
            else:
                raise

# Use the function to search arXiv and get a DataFrame of results
df = search_arxiv(QUERY)
if df.empty: 
    raise SystemExit("No results. Try a broader query or increase max_results.")

# Combine title + abstract as the unit of meaning
df["text"] = df["title"].astype(str) + ". " + df["summary"].astype(str)

os.makedirs("query-results", exist_ok=True)
out_path = os.path.join("query-results", "results.csv")
df.to_csv(out_path, index=False)
print(f"Results saved to {out_path}")

# -----------------