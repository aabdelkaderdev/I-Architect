<!-- Source: https://docs.langchain.com/oss/python/integrations/document_loaders/huawei_obs_file -->

The following code demonstrates how to load an object from the Huawei OBS (Object Storage Service) as document.

Copy

```
# Install the required package
# pip install esdk-obs-python
```

Copy

```
from langchain_community.document_loaders.obs_file import OBSFileLoader
```

Copy

```
endpoint = "your-endpoint"
```

Copy

```
from obs import ObsClient

obs_client = ObsClient(
    access_key_id="your-access-key",
    secret_access_key="your-secret-key",
    server=endpoint,
)
loader = OBSFileLoader("your-bucket-name", "your-object-key", client=obs_client)
```

Copy

```
loader.load()
```

## [​](#each-loader-with-separate-authentication-information) Each loader with separate authentication information

If you don’t need to reuse OBS connections between different loaders, you can directly configure the `config`. The loader will use the config information to initialize its own OBS client.

Copy

```
# Configure your access credentials\n
config = {"ak": "your-access-key", "sk": "your-secret-key"}
loader = OBSFileLoader(
    "your-bucket-name", "your-object-key", endpoint=endpoint, config=config
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
loader = OBSFileLoader(
    "your-bucket-name", "your-object-key", endpoint=endpoint, config=config
)
```

Copy

```
loader.load()
```

## [​](#access-a-publicly-accessible-object) Access a publicly accessible object

If the object you want to access allows anonymous user access (anonymous users have `GetObject` permission), you can directly load the object without configuring the `config` parameter.

Copy

```
loader = OBSFileLoader("your-bucket-name", "your-object-key", endpoint=endpoint)
```

Copy

```
loader.load()
```

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/document_loaders/huawei_obs_file.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.