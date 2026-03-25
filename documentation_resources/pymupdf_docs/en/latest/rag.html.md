<!-- Source: https://pymupdf.readthedocs.io/en/latest/rag.html -->

pymupdf.io

[English](javaScript:changeLanguage('en'))
[日本語](javaScript:changeLanguage('ja'))
[한국어](javaScript:changeLanguage('ko'))

[Find **#pymupdf** on **Discord**](https://discord.gg/TSpYGBW4eq)

[Try our forum!](https://forum.mupdf.com)

# PyMuPDF, LLM & RAG

Integrating PyMuPDF into your Large Language Model (LLM) framework and overall RAG (Retrieval-Augmented Generation) solution provides the fastest and most reliable way to deliver document data.

There are a few well known LLM solutions which have their own interfaces with PyMuPDF - it is a fast growing area, so please let us know if you discover any more!

If you need to export to Markdown or obtain a LlamaIndex Document from a file:

Try PyMuPDF4LLM

## Integration with LangChain

It is simple to integrate directly with LangChain by using their dedicated loader as follows:

```
from langchain_community.document_loaders import PyMuPDFLoader
loader = PyMuPDFLoader("example.pdf")
data = loader.load()
```

See [LangChain Using PyMuPDF](https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf/#using-pymupdf) for full details.

## Integration with LlamaIndex

Use the dedicated `PyMuPDFReader` from LlamaIndex 🦙 to manage your document loading.

```
from llama_index.readers.file import PyMuPDFReader
loader = PyMuPDFReader()
documents = loader.load(file_path="example.pdf")
```

See [Building RAG from Scratch](https://docs.llamaindex.ai/en/stable/examples/low_level/oss_ingestion_retrieval) for more.

## Preparing Data for Chunking

Chunking (or splitting) data is essential to give context to your LLM data and with Markdown output now supported by PyMuPDF this means that [Level 3 chunking](https://medium.com/@anuragmishra_27746/five-levels-of-chunking-strategies-in-rag-notes-from-gregs-video-7b735895694d#b123) is supported.

### Outputting as Markdown

In order to export your document in Markdown format you will need a separate helper. Package [PyMuPDF4LLM](pymupdf4llm/index.html) is a high-level wrapper of PyMuPDF functions which for each page outputs standard and table text in an integrated Markdown-formatted string across all document pages:

```
# convert the document to markdown
import pymupdf4llm
md_text = pymupdf4llm.to_markdown("input.pdf")

# Write the text to some file in UTF8-encoding
import pathlib
pathlib.Path("output.md").write_bytes(md_text.encode())
```

For further information please refer to: [PyMuPDF4LLM](pymupdf4llm/index.html).

### How to use Markdown output

Once you have your data in Markdown format you are ready to chunk/split it and supply it to your LLM, for example, if this is LangChain then do the following:

```
import pymupdf4llm
from langchain.text_splitter import MarkdownTextSplitter

# Get the MD text
md_text = pymupdf4llm.to_markdown("input.pdf")  # get markdown for all pages

splitter = MarkdownTextSplitter(chunk_size=40, chunk_overlap=0)

splitter.create_documents([md_text])
```

For more see [5 Levels of Text Splitting](https://github.com/FullStackRetrieval-com/RetrievalTutorials/blob/main/tutorials/LevelsOfTextSplitting/5_Levels_Of_Text_Splitting.ipynb)

## Related Blogs

To find out more about PyMuPDF, LLM & RAG check out our blogs for implementations & tutorials.

### Methodologies to Extract Text

- [Enhanced Text Extraction](https://artifex.com/blog/rag-llm-and-pdf-enhanced-text-extraction)
- [Conversion to Markdown Text with PyMuPDF](https://artifex.com/blog/rag-llm-and-pdf-conversion-to-markdown-text-with-pymupdf)

### Create a Chatbot to discuss your documents

- [Make a simple command line Chatbot](https://artifex.com/blog/creating-a-rag-chatbot-with-chatgpt-and-pymupdf)
- [Make a Chatbot GUI](https://artifex.com/blog/building-a-rag-chatbot-gui-with-the-chatgpt-api-and-pymupdf)

---

This software is provided AS-IS with no warranty, either express or implied. This software is distributed under license and may not be copied, modified or distributed except as expressly authorized under the terms of that license. Refer to licensing information at [artifex.com](https://www.artifex.com?utm_source=rtd-pymupdf&utm_medium=rtd&utm_content=footer-link) or contact Artifex Software Inc., 39 Mesa Street, Suite 108A, San Francisco CA 94129, United States for further information.