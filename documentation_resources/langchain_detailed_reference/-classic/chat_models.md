<!-- Source: https://reference.langchain.com/python/langchain-classic/chat_models -->

Modulev1.2.13 (latest)●Since v1.0

# chat\_models

**Chat Models** are a variation on language models.

While Chat Models use language models under the hood, the interface they expose
is a bit different. Rather than expose a "text in, text out" API, they expose
an interface where "chat messages" are the inputs and outputs.

## Functions

[function

is\_interactive\_env

Determine if running within IPython or Jupyter.](/python/langchain-classic/_api/interactive_env/is_interactive_env)[function

init\_chat\_model

Initialize a chat model from any supported provider using a unified interface.

**Two main use cases:**

1. **Fixed model** – specify the model upfront and get back a ready-to-use chat
   model.
2. **Configurable model** – choose to specify parameters (including model name) at
   runtime via `config`. Makes it easy to switch between models/providers without
   changing your code

Note

Requires the integration package for the chosen model provider to be installed.

See the `model_provider` parameter below for specific package names
(e.g., `pip install langchain-openai`).

Refer to the [provider integration's API reference](https://docs.langchain.com/oss/python/integrations/providers)
for supported model parameters to use as `**kwargs`.](/python/langchain-classic/chat_models/base/init_chat_model)

## Modules

[module

baidu\_qianfan\_endpoint](/python/langchain-classic/chat_models/baidu_qianfan_endpoint)[module

yandex](/python/langchain-classic/chat_models/yandex)[module

azureml\_endpoint](/python/langchain-classic/chat_models/azureml_endpoint)[module

cohere](/python/langchain-classic/chat_models/cohere)[module

promptlayer\_openai](/python/langchain-classic/chat_models/promptlayer_openai)[module

litellm](/python/langchain-classic/chat_models/litellm)[module

javelin\_ai\_gateway](/python/langchain-classic/chat_models/javelin_ai_gateway)[module

base](/python/langchain-classic/chat_models/base)[module

baichuan](/python/langchain-classic/chat_models/baichuan)[module

hunyuan](/python/langchain-classic/chat_models/hunyuan)[module

mlflow\_ai\_gateway](/python/langchain-classic/chat_models/mlflow_ai_gateway)[module

ollama](/python/langchain-classic/chat_models/ollama)[module

fake](/python/langchain-classic/chat_models/fake)[module

pai\_eas\_endpoint](/python/langchain-classic/chat_models/pai_eas_endpoint)[module

azure\_openai](/python/langchain-classic/chat_models/azure_openai)[module

vertexai](/python/langchain-classic/chat_models/vertexai)[module

konko](/python/langchain-classic/chat_models/konko)[module

human](/python/langchain-classic/chat_models/human)[module

gigachat](/python/langchain-classic/chat_models/gigachat)[module

fireworks](/python/langchain-classic/chat_models/fireworks)[module

google\_palm](/python/langchain-classic/chat_models/google_palm)[module

openai](/python/langchain-classic/chat_models/openai)[module

tongyi](/python/langchain-classic/chat_models/tongyi)[module

volcengine\_maas](/python/langchain-classic/chat_models/volcengine_maas)[module

ernie](/python/langchain-classic/chat_models/ernie)[module

minimax](/python/langchain-classic/chat_models/minimax)[module

jinachat](/python/langchain-classic/chat_models/jinachat)[module

bedrock](/python/langchain-classic/chat_models/bedrock)[module

anthropic](/python/langchain-classic/chat_models/anthropic)[module

meta](/python/langchain-classic/chat_models/meta)[module

databricks](/python/langchain-classic/chat_models/databricks)[module

everlyai](/python/langchain-classic/chat_models/everlyai)[module

mlflow](/python/langchain-classic/chat_models/mlflow)[module

anyscale](/python/langchain-classic/chat_models/anyscale)


