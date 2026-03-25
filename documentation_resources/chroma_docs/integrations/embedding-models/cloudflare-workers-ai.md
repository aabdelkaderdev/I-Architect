<!-- Source: https://docs.trychroma.com/integrations/embedding-models/cloudflare-workers-ai -->

Chroma provides a wrapper around Cloudflare Workers AI embedding models. This embedding function runs remotely against the Cloudflare Workers AI servers, and will require an API key and a Cloudflare account. You can find more information in the [Cloudflare Workers AI Docs](https://developers.cloudflare.com/workers-ai/).
You can also optionally use the Cloudflare AI Gateway for a more customized solution by setting a `gateway_id` argument. See the [Cloudflare AI Gateway Docs](https://developers.cloudflare.com/ai-gateway/providers/workersai/) for more info.

Python

TypeScript

Report incorrect code

Copy

Ask AI

```
from chromadb.utils.embedding_functions import CloudflareWorkersAIEmbeddingFunction

os.environ["CHROMA_CLOUDFLARE_API_KEY"] = "<INSERT API KEY HERE>"

ef = CloudflareWorkersAIEmbeddingFunction(
    account_id="<INSERT ACCOUNTID HERE>",
    model_name="@cf/baai/bge-m3",
)
ef(input=["This is my first text to embed", "This is my second document"])
```

You must pass in an `account_id` and `model_name` to the embedding function. It is recommended to set the `CHROMA_CLOUDFLARE_API_KEY` for the api key, but the embedding function also optionally takes in an `api_key` variable.