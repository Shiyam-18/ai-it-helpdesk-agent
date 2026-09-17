# Architecture Notes

## Request flow

1. User submits an IT issue in Streamlit.
2. `KnowledgeBase.search()` embeds the question.
3. Cosine similarity ranks the local knowledge-base documents.
4. The top matching articles are added to the LLM prompt.
5. Gemini receives the prompt and function tools.
6. Gemini may call `check_internet_connection`, `get_system_info`, or `create_support_ticket`.
7. The Python SDK executes those tools and sends results back automatically.
8. Gemini produces the final user-facing answer.
9. Streamlit displays the answer, retrieved source names, and tool activity.

## Why this qualifies

The project intentionally keeps the implementation small while showing the three required capabilities:

- Agent: model-driven tool selection and response generation.
- RAG: retrieval from a local embedded troubleshooting knowledge base.
- Tools: executable Python functions exposed to the model.
