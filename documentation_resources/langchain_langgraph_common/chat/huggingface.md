<!-- Source: https://docs.langchain.com/oss/python/integrations/chat/huggingface -->

This will help you get started with `langchain_huggingface` [chat models](/oss/python/langchain/models). For detailed documentation of all `ChatHuggingFace` features and configurations head to the [API reference](https://python.langchain.com/api_reference/huggingface/chat_models/langchain_huggingface.chat_models.huggingface.ChatHuggingFace.html). For a list of models supported by Hugging Face check out [this page](https://huggingface.co/models).

## [​](#overview) Overview

### [​](#integration-details) Integration details

| Class | Package | Serializable | JS support | Downloads | Version |
| --- | --- | --- | --- | --- | --- |
| [ChatHuggingFace](https://python.langchain.com/api_reference/huggingface/chat_models/langchain_huggingface.chat_models.huggingface.ChatHuggingFace.html) | [langchain-huggingface](https://python.langchain.com/api_reference/huggingface/index.html) | beta | ❌ |  |  |

### [​](#model-features) Model features

| [Tool calling](/oss/python/langchain/tools) | [Structured output](/oss/python/langchain/structured-output) | [Image input](/oss/python/langchain/messages#multimodal) | Audio input | Video input | [Token-level streaming](/oss/python/langchain/streaming) | Native async | [Token usage](/oss/python/langchain/models#token-usage) | [Logprobs](/oss/python/langchain/models#log-probabilities) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ |

## [​](#setup) Setup

To access Hugging Face models you’ll need to create a Hugging Face account, get an API key, and install the `langchain-huggingface` integration package.

### [​](#credentials) Credentials

Generate a [Hugging Face Access Token](https://huggingface.co/docs/hub/security-tokens) and store it as an environment variable: `HUGGINGFACEHUB_API_TOKEN`.

Copy

```
import getpass
import os

if not os.getenv("HUGGINGFACEHUB_API_TOKEN"):
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = getpass.getpass("Enter your token: ")
```

### [​](#installation) Installation

| Class | Package | Serializable | JS support | Downloads | Version |
| --- | --- | --- | --- | --- | --- |
| [ChatHuggingFace](https://python.langchain.com/api_reference/huggingface/chat_models/langchain_huggingface.chat_models.huggingface.ChatHuggingFace.html) | [langchain-huggingface](https://python.langchain.com/api_reference/huggingface/index.html) | ❌ | ❌ |  |  |

### [​](#model-features-2) Model features

| [Tool calling](/oss/python/langchain/tools) | [Structured output](/oss/python/langchain/structured-output) | [Image input](/oss/python/langchain/messages#multimodal) | Audio input | Video input | [Token-level streaming](/oss/python/langchain/streaming) | Native async | [Token usage](/oss/python/langchain/models#token-usage) | [Logprobs](/oss/python/langchain/models#log-probabilities) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

## [​](#setup-2) Setup

To access `langchain_huggingface` models you’ll need to create a `Hugging Face` account, get an API key, and install the `langchain-huggingface` integration package.

### [​](#credentials-2) Credentials

You’ll need to have a [Hugging Face Access Token](https://huggingface.co/docs/hub/security-tokens) saved as an environment variable: `HUGGINGFACEHUB_API_TOKEN`.

Copy

```
import getpass
import os

os.environ["HUGGINGFACEHUB_API_TOKEN"] = getpass.getpass(
    "Enter your Hugging Face API key: "
)
```

Copy

```
pip install -qU  langchain-huggingface text-generation transformers google-search-results numexpr langchainhub sentencepiece jinja2 bitsandbytes accelerate
```

## [​](#instantiation) Instantiation

You can instantiate a `ChatHuggingFace` model in two different ways, either from a `HuggingFaceEndpoint` or from a `HuggingFacePipeline`.

### [​](#huggingfaceendpoint) `HuggingFaceEndpoint`

Copy

```
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-R1-0528",
    task="text-generation",
    max_new_tokens=512,
    do_sample=False,
    repetition_penalty=1.03,
    provider="auto",  # let Hugging Face choose the best provider for you
)

chat_model = ChatHuggingFace(llm=llm)
```

Copy

```
The token has not been saved to the git credentials helper. Pass `add_to_git_credential=True` in this function directly or `--add-to-git-credential` if using via `huggingface-cli` if you want to set the git credential as well.
Token is valid (permission: fineGrained).
Your token has been saved to /Users/isaachershenson/.cache/huggingface/token
Login successful
```

Now let’s take advantage of [Inference Providers](https://huggingface.co/docs/inference-providers) to run the model on specific third-party providers

Copy

```
llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-R1-0528",
    task="text-generation",
    provider="hyperbolic",  # set your provider here
    # provider="nebius",
    # provider="together",
)

chat_model = ChatHuggingFace(llm=llm)
```

### [​](#huggingfacepipeline) `HuggingFacePipeline`

Copy

```
from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline

llm = HuggingFacePipeline.from_model_id(
    model_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",
    pipeline_kwargs=dict(
        max_new_tokens=512,
        do_sample=False,
        repetition_penalty=1.03,
    ),
)

chat_model = ChatHuggingFace(llm=llm)
```

Copy

```
config.json:   0%|          | 0.00/638 [00:00<?, ?B/s]
```

Copy

```
model.safetensors.index.json:   0%|          | 0.00/23.9k [00:00<?, ?B/s]
```

Copy

```
Downloading shards:   0%|          | 0/8 [00:00<?, ?it/s]
```

Copy

```
model-00001-of-00008.safetensors:   0%|          | 0.00/1.89G [00:00<?, ?B/s]
```

Copy

```
model-00002-of-00008.safetensors:   0%|          | 0.00/1.95G [00:00<?, ?B/s]
```

Copy

```
model-00003-of-00008.safetensors:   0%|          | 0.00/1.98G [00:00<?, ?B/s]
```

Copy

```
model-00004-of-00008.safetensors:   0%|          | 0.00/1.95G [00:00<?, ?B/s]
```

Copy

```
model-00005-of-00008.safetensors:   0%|          | 0.00/1.98G [00:00<?, ?B/s]
```

Copy

```
model-00006-of-00008.safetensors:   0%|          | 0.00/1.95G [00:00<?, ?B/s]
```

Copy

```
model-00007-of-00008.safetensors:   0%|          | 0.00/1.98G [00:00<?, ?B/s]
```

Copy

```
model-00008-of-00008.safetensors:   0%|          | 0.00/816M [00:00<?, ?B/s]
```

Copy

```
Loading checkpoint shards:   0%|          | 0/8 [00:00<?, ?it/s]
```

Copy

```
generation_config.json:   0%|          | 0.00/111 [00:00<?, ?B/s]
```

### [​](#instatiating-with-quantization) Instatiating with quantization

To run a quantized version of your model, you can specify a `bitsandbytes` quantization config as follows:

Copy

```
from transformers import BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype="float16",
    bnb_4bit_use_double_quant=True,
)
```

and pass it to the `HuggingFacePipeline` as a part of its `model_kwargs`:

Copy

```
llm = HuggingFacePipeline.from_model_id(
    model_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",
    pipeline_kwargs=dict(
        max_new_tokens=512,
        do_sample=False,
        repetition_penalty=1.03,
        return_full_text=False,
    ),
    model_kwargs={"quantization_config": quantization_config},
)

chat_model = ChatHuggingFace(llm=llm)
```

## [​](#invocation) Invocation

Copy

```
from langchain.messages import (
    HumanMessage,
    SystemMessage,
)

messages = [
    SystemMessage(content="You're a helpful assistant"),
    HumanMessage(
        content="What happens when an unstoppable force meets an immovable object?"
    ),
]

ai_msg = chat_model.invoke(messages)
```

Copy

```
print(ai_msg.content)
```

Copy

```
According to the popular phrase and hypothetical scenario, when an unstoppable force meets an immovable object, a paradoxical situation arises as both forces are seemingly contradictory. On one hand, an unstoppable force is an entity that cannot be stopped or prevented from moving forward, while on the other hand, an immovable object is something that cannot be moved or displaced from its position.

In this scenario, it is un
```

---

## [​](#api-reference) API reference

For detailed documentation of all `ChatHuggingFace` features and configurations head to the API reference: [python.langchain.com/api\_reference/huggingface/chat\_models/langchain\_huggingface.chat\_models.huggingface.ChatHuggingFace.html](https://python.langchain.com/api_reference/huggingface/chat_models/langchain_huggingface.chat_models.huggingface.ChatHuggingFace.html)

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/chat/huggingface.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.