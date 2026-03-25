<!-- Source: https://reference.langchain.com/python/langchain-classic/evaluation/loading/load_dataset -->

Functionv1.2.13 (latest)●Since v1.0

# load\_dataset

Load a dataset from the [LangChainDatasets on HuggingFace](https://huggingface.co/LangChainDatasets).


```
load_dataset(
    uri: str,
) -> list[dict]
```

**Prerequisites**

```
pip install datasets
```

## Examples:

```
from langchain_classic.evaluation import load_dataset

ds = load_dataset("llm-math")
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `uri`\* | `str` | The uri of the dataset to load. |


