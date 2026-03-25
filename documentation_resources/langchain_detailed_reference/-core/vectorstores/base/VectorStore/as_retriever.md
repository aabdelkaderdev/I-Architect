<!-- Source: https://reference.langchain.com/python/langchain-core/vectorstores/base/VectorStore/as_retriever -->

Methodv1.2.21 (latest)●Since v0.2

# as\_retriever

Return `VectorStoreRetriever` initialized from this `VectorStore`.


```
as_retriever(
    self,
    **kwargs: Any = {},
) -> VectorStoreRetriever
```

Examples:

```
# Retrieve more documents with higher diversity
# Useful if your dataset has many similar documents
docsearch.as_retriever(
    search_type="mmr", search_kwargs={"k": 6, "lambda_mult": 0.25}
)

# Fetch more documents for the MMR algorithm to consider
# But only return the top 5
docsearch.as_retriever(search_type="mmr", search_kwargs={"k": 5, "fetch_k": 50})

# Only retrieve documents that have a relevance score
# Above a certain threshold
docsearch.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"score_threshold": 0.8},
)

# Only get the single most similar document from the dataset
docsearch.as_retriever(search_kwargs={"k": 1})

# Use a filter to only retrieve documents from a specific paper
docsearch.as_retriever(
    search_kwargs={"filter": {"paper_title": "GPT-4 Technical Report"}}
)
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `**kwargs` | `Any` | Default:`{}`  Keyword arguments to pass to the search function.  Can include:   - `search_type`: Defines the type of search that the Retriever should   perform. Can be `'similarity'` (default), `'mmr'`, or   `'similarity_score_threshold'`. - `search_kwargs`: Keyword arguments to pass to the search function.  Can include things like:    - `k`: Amount of documents to return (Default: `4`)   - `score_threshold`: Minimum relevance threshold     for `similarity_score_threshold`   - `fetch_k`: Amount of documents to pass to MMR algorithm     (Default: `20`)   - `lambda_mult`: Diversity of results returned by MMR;     `1` for minimum diversity and 0 for maximum. (Default: `0.5`)   - `filter`: Filter by document metadata |


