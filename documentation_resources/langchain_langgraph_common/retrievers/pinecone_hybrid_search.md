<!-- Source: https://docs.langchain.com/oss/python/integrations/retrievers/pinecone_hybrid_search -->

> [Pinecone](https://docs.pinecone.io/docs/overview) is a vector database with broad functionality.

This notebook goes over how to use a retriever that under the hood uses Pinecone and Hybrid Search.
The logic of this retriever is taken from [this documentation](https://docs.pinecone.io/docs/hybrid-search)
To use Pinecone, you must have an API key and an Environment.
Here are the [installation instructions](https://docs.pinecone.io/docs/quickstart).

Copy

```
pip install -qU  pinecone pinecone-text pinecone-notebooks
```

Copy

```
# Connect to Pinecone and get an API key.
from pinecone_notebooks.colab import Authenticate

Authenticate()

import os

api_key = os.environ["PINECONE_API_KEY"]
```

Copy

```
from langchain_community.retrievers import (
    PineconeHybridSearchRetriever,
)
```

We want to use `OpenAIEmbeddings` so we have to get the OpenAI API Key.

Copy

```
import getpass

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
```

## [​](#setup-pinecone) Setup pinecone

You should only have to do this part once.

Copy

```
import os

from pinecone import Pinecone, ServerlessSpec

index_name = "langchain-pinecone-hybrid-search"

# initialize Pinecone client
pc = Pinecone(api_key=api_key)

# create the index
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # dimensionality of dense model
        metric="dotproduct",  # sparse values supported only for dotproduct
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
```

Copy

```
WhoAmIResponse(username='load', user_label='label', projectname='load-test')
```

Now that the index is created, we can use it.

Copy

```
index = pc.Index(index_name)
```

## [​](#get-embeddings-and-sparse-encoders) Get embeddings and sparse encoders

Embeddings are used for the dense vectors, tokenizer is used for the sparse vector

Copy

```
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
```

To encode the text to sparse values you can either choose SPLADE or BM25. For out of domain tasks we recommend using BM25.
For more information about the sparse encoders you can checkout pinecone-text library [docs](https://pinecone-io.github.io/pinecone-text/pinecone_text.html).

Copy

```
from pinecone_text.sparse import BM25Encoder

# or from pinecone_text.sparse import SpladeEncoder if you wish to work with SPLADE

# use default tf-idf values
bm25_encoder = BM25Encoder().default()
```

The above code is using default tfids values. It’s highly recommended to fit the tf-idf values to your own corpus. You can do it as follow:

Copy

```
corpus = ["foo", "bar", "world", "hello"]

# fit tf-idf values on your corpus
bm25_encoder.fit(corpus)

# store the values to a json file
bm25_encoder.dump("bm25_values.json")

# load to your BM25Encoder object
bm25_encoder = BM25Encoder().load("bm25_values.json")
```

## [​](#load-retriever) Load retriever

We can now construct the retriever!

Copy

```
retriever = PineconeHybridSearchRetriever(
    embeddings=embeddings, sparse_encoder=bm25_encoder, index=index
)
```

## [​](#add-texts-if-necessary) Add texts (if necessary)

We can optionally add texts to the retriever (if they aren’t already in there)

Copy

```
retriever.add_texts(["foo", "bar", "world", "hello"])
```

Copy

```
100%|██████████| 1/1 [00:02<00:00,  2.27s/it]
```

## [​](#use-retriever) Use retriever

We can now use the retriever!

Copy

```
result = retriever.invoke("foo")
```

Copy

```
result[0]
```

Copy

```
Document(page_content='foo', metadata={})
```

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/retrievers/pinecone_hybrid_search.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.