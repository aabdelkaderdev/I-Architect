<!-- Source: https://docs.langchain.com/oss/python/integrations/document_loaders/huawei_obs_directory -->

The following code demonstrates how to load objects from the Huawei OBS (Object Storage Service) as documents.

Copy

```
# Install the required package
# pip install esdk-obs-python
```

Copy

```
from langchain_community.document_loaders import OBSDirectoryLoader
```

Copy

```
endpoint = "your-endpoint"
```

Copy

```
# Configure your access credentials\n
config = {"ak": "your-access-key", "sk": "your-secret-key"}
loader = OBSDirectoryLoader("your-bucket-name", endpoint=endpoint, config=config)
```

Copy

```
loader.load()
```

## [​](#specify-a-prefix-for-loading) Specify a prefix for loading

If you want to load objects with a specific prefix from the bucket, you can use the following code:

Copy

```
loader = OBSDirectoryLoader(
    "your-bucket-name", endpoint=endpoint, config=config, prefix="test_prefix"
)
```

Copy

```
loader.load()
```

## [​](#get-authentication-information-from-ecs) Get authentication information from ECS

If your langchain is deployed on Huawei Cloud ECS and [Agency is set up](https://support.huaweicloud.com/intl/en-us/usermanual-ecs/ecs_03_0166.html#section7), the loader can directly get the security token from ECS without needing access key and secret key.

Copy

```
config = {"get_token_from_ecs": True}
loader = OBSDirectoryLoader("your-bucket-name", endpoint=endpoint, config=config)
```

Copy

```
loader.load()
```

## [​](#use-a-public-bucket) Use a public bucket

If your bucket’s bucket policy allows anonymous access (anonymous users have `listBucket` and `GetObject` permissions), you can directly load the objects without configuring the `config` parameter.

Copy

```
loader = OBSDirectoryLoader("your-bucket-name", endpoint=endpoint)
```

Copy

```
loader.load()
```

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/document_loaders/huawei_obs_directory.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.