<!-- Source: https://docs.trychroma.com/integrations/embedding-models/amazon-bedrock -->

This embedding function relies on the boto3 python package, which you can install with pip install boto3.

Python

Report incorrect code

Copy

Ask AI

```
import boto3
from chromadb.utils.embedding_functions import AmazonBedrockEmbeddingFunction

session = boto3.Session(profile_name="profile", region_name="us-east-1")
bedrock_ef = AmazonBedrockEmbeddingFunction(
    session=session,
    model_name="amazon.titan-embed-text-v1"
)

texts = ["Hello, world!", "How are you?"]
embeddings = bedrock_ef(texts)
```

You can pass in an optional model\_name argument, which lets you choose which Amazon Bedrock embedding model to use. By default, Chroma uses amazon.titan-embed-text-v1.

Visit Amazon Bedrock [documentation](https://docs.aws.amazon.com/bedrock/) for more information on available models and configuration.