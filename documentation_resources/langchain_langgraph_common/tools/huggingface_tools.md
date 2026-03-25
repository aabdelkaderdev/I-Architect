<!-- Source: https://docs.langchain.com/oss/python/integrations/tools/huggingface_tools -->

> [Huggingface Tools](https://huggingface.co/docs/transformers/v4.29.0/en/custom_tools) that supporting text I/O can be
> loaded directly using the `load_huggingface_tool` function.

Copy

```
# Requires transformers>=4.29.0 and huggingface_hub>=0.14.1
pip install -qU  transformers huggingface_hub > /dev/null
```

Copy

```
pip install -qU  langchain-community
```

Copy

```
from langchain_community.agent_toolkits.load_tools import load_huggingface_tool

tool = load_huggingface_tool("lysandre/hf-model-downloads")

print(f"{tool.name}: {tool.description}")
```

Copy

```
model_download_counter: This is a tool that returns the most downloaded model of a given task on the Hugging Face Hub. It takes the name of the category (such as text-classification, depth-estimation, etc), and returns the name of the checkpoint
```

Copy

```
tool.run("text-classification")
```

Copy

```
'facebook/bart-large-mnli'
```

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/tools/huggingface_tools.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.