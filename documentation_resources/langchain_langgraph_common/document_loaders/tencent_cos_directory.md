<!-- Source: https://docs.langchain.com/oss/python/integrations/document_loaders/tencent_cos_directory -->

> [Tencent Cloud Object Storage (COS)](https://www.tencentcloud.com/products/cos) is a distributed
> storage service that enables you to store any amount of data from anywhere via HTTP/HTTPS protocols.
> `COS` has no restrictions on data structure or format. It also has no bucket size limit and
> partition management, making it suitable for virtually any use case, such as data delivery,
> data processing, and data lakes. `COS` provides a web-based console, multi-language SDKs and APIs,
> command line tool, and graphical tools. It works well with Amazon S3 APIs, allowing you to quickly
> access community tools and plugins.

This covers how to load document objects from a `Tencent COS Directory`.

Copy

```
pip install -qU  cos-python-sdk-v5
```

Copy

```
from langchain_community.document_loaders import TencentCOSDirectoryLoader
from qcloud_cos import CosConfig
```

Copy

```
conf = CosConfig(
    Region="your cos region",
    SecretId="your cos secret_id",
    SecretKey="your cos secret_key",
)
loader = TencentCOSDirectoryLoader(conf=conf, bucket="you_cos_bucket")
```

Copy

```
loader.load()
```

## [​](#specifying-a-prefix) Specifying a prefix

You can also specify a prefix for more fine-grained control over what files to load.

Copy

```
loader = TencentCOSDirectoryLoader(conf=conf, bucket="you_cos_bucket", prefix="fake")
```

Copy

```
loader.load()
```

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/document_loaders/tencent_cos_directory.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.