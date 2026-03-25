<!-- Source: https://docs.langchain.com/oss/python/integrations/llms/cohere -->

**You are currently on a page documenting the use of Cohere models as text completion models. Many popular Cohere models are [chat completion models](/oss/python/langchain/models).**You may be looking for [this page instead](/oss/python/integrations/chat/cohere).

> [Cohere](https://cohere.ai/about) is a Canadian startup that provides natural language processing models that help companies improve human-machine interactions.

Head to the [API reference](https://python.langchain.com/api_reference/community/llms/langchain_community.llms.cohere.Cohere.html) for detailed documentation of all attributes and methods.

## [​](#overview) Overview

### [​](#integration-details) Integration details

| Class | Package | Local | Serializable | [JS support](https://js.langchain.com/docs/integrations/llms/cohere/) | Downloads | Version |
| --- | --- | --- | --- | --- | --- | --- |
| [Cohere](https://python.langchain.com/api_reference/community/llms/langchain_community.llms.cohere.Cohere.html) | [langchain-community](https://python.langchain.com/api_reference/community/index.html) | ❌ | beta | ✅ |  |  |

## [​](#setup) Setup

The integration lives in the `langchain-community` package. We also need to install the `cohere` package itself. We can install these with:

### [​](#credentials) Credentials

We’ll need to get a [Cohere API key](https://cohere.com/) and set the `COHERE_API_KEY` environment variable:

Copy

```
import getpass
import os

if "COHERE_API_KEY" not in os.environ:
    os.environ["COHERE_API_KEY"] = getpass.getpass()
```

### [​](#installation) Installation

Copy

```
pip install -U langchain-community langchain-cohere
```

It’s also helpful (but not needed) to set up [LangSmith](https://smith.langchain.com/) for best-in-class observability

Copy

```
os.environ["LANGSMITH_TRACING"] = "true"
# os.environ["LANGSMITH_API_KEY"] = getpass.getpass()
```

## [​](#invocation) Invocation

Cohere supports all [LLM](/oss/python/langchain/models) functionality:

Copy

```
from langchain_cohere import Cohere
from langchain.messages import HumanMessage
```

Copy

```
model = Cohere(max_tokens=256, temperature=0.75)
```

Copy

```
message = "Knock knock"
model.invoke(message)
```

Copy

```
" Who's there?"
```

Copy

```
await model.ainvoke(message)
```

Copy

```
" Who's there?"
```

Copy

```
for chunk in model.stream(message):
    print(chunk, end="", flush=True)
```

Copy

```
 Who's there?
```

Copy

```
model.batch([message])
```

Copy

```
[" Who's there?"]
```

---

## [​](#api-reference) API reference

For detailed documentation of all `Cohere` llm features and configurations head to the API reference: [python.langchain.com/api\_reference/community/llms/langchain\_community.llms.cohere.Cohere.html](https://python.langchain.com/api_reference/community/llms/langchain_community.llms.cohere.Cohere.html)

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/llms/cohere.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.