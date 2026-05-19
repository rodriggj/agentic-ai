RAG Pipeline
=============

This repository contains a small Retrieval-Augmented Generation (RAG) pipeline using LangChain.

Files
-----
- `rag-pipeline.py`: Main script. Accepts CLI arguments and runs the RAG flow.
- `requirements.txt`: Python dependencies.
- `tests/`: Unit tests for core helper functions.

Quickstart
----------
1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set your OpenAI API key in the environment:

```bash
export OPENAI_API_KEY="sk-..."
```

4. Run the pipeline (query is required):

```bash
python rag-pipeline.py -q "What are the main limitations of retrieval-augmented generation?" --docs-path ./docs --verbose

or 

(explicit)
cd /Users/gabrrodriguez/Desktop/agentic-ai/1_knowledge-retrieval-agents
.venv/bin/python rag-pipeline.py -q "Compare contrast..." --docs-path ./docs --verbose
```

Running tests
-------------
Install test dependencies (already included in `requirements.txt`) and run:

```bash
pytest -q
```

Notes
-----
- Tests load `rag-pipeline.py` directly from the filesystem using importlib; the script remains executable as a standalone program.
- The unit tests mock out expensive operations where practical; they focus on small, testable helper functions.
- If you want expanded coverage or integration tests that actually call OpenAI, let me know and I can add a test harness and CI config.

To deactivate the `.venv` run the following: 

```bash
deactivate
```