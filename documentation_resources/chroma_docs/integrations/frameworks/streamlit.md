<!-- Source: https://docs.trychroma.com/integrations/frameworks/streamlit -->

Streamlit is an open-source Python library that makes it easy to create and share beautiful, custom web apps for machine learning and data science. In just a few minutes you can build and deploy powerful data apps.

[Apache 2.0 License](https://github.com/streamlit/streamlit/blob/develop/LICENSE) | [Site](https://streamlit.io/)

| Languages | Docs | Github |
| --- | --- | --- |
| Python | [Docs](https://docs.streamlit.io/) | [Code](https://github.com/streamlit/streamlit) |

### [​](#install) Install

Install Streamlit:
`pip install streamlit`
Install `streamlit-chromadb-connection`, which connects your Streamlit app to Chroma through [`st.connection`](https://docs.streamlit.io/1.11.0/library/api-reference/connections/st.connection):
`pip install streamlit-chromadb-connection`

### [​](#main-benefits) Main Benefits

- Easy to get started with Streamlit’s straightforward syntax
- Built-in [chatbot functionality](https://docs.streamlit.io/library/api-reference/chat)
- Pre-built integration with Chroma via `streamlit-chromadb-connection`
- Deploy apps for free on [Streamlit Community Cloud](https://share.streamlit.io/)

### [​](#simple-example) Simple Example

#### [​](#python) Python

Report incorrect code

Copy

Ask AI

```
import streamlit as st
from streamlit_chromadb_connection.chromadb_connection import ChromadbConnection

configuration = {
    "client": "PersistentClient",
    "path": "/tmp/.chroma"
}

collection_name = "documents_collection"

conn = st.connection("chromadb",
                     type=ChromaDBConnection,
                     **configuration)
documents_collection_df = conn.get_collection_data(collection_name)
st.dataframe(documents_collection_df)
```

### [​](#resources) Resources

- [Instructions for using `streamlit-chromadb-connection` to connect your Streamlit app to Chroma](https://github.com/Dev317/streamlit_chromadb_connection/blob/main/README.md)
- [Demo app for `streamlit-chromadb-connection`](https://app-chromadbconnection-mfzxl3nzozmaxh3mrkd6zm.streamlit.app/)
- [Streamlit’s `st.connection` documentation](https://docs.streamlit.io/library/api-reference/connections/st.connection)
- [Guide to using vector databases with Streamlit](https://pub.towardsai.net/vector-databases-for-your-streamlit-ai-apps-56cd0af7bbba)

#### [​](#tutorials) Tutorials

- [Build an “Ask the Doc” app using Chroma, Streamlit, and LangChain](https://blog.streamlit.io/langchain-tutorial-4-build-an-ask-the-doc-app/)
- [Summarize documents with Chroma, Streamlit, and LangChain](https://alphasec.io/summarize-documents-with-langchain-and-chroma/)
- [Build a custom chatbot with Chroma, Streamlit, and LangChain](https://blog.streamlit.io/how-in-app-feedback-can-increase-your-chatbots-performance/)
- [Build a RAG bot using Chroma, Streamlit, and LangChain](https://levelup.gitconnected.com/building-a-generative-ai-app-with-streamlit-and-openai-95ec31fe8efd)
- [Build a PDF QA chatbot with Chroma, Streamlit, and OpenAI](https://www.confident-ai.com/blog/how-to-build-a-pdf-qa-chatbot-using-openai-and-chromadb)