<!-- Source: https://docs.langchain.com/oss/python/integrations/providers/redis -->

> [Redis (Remote Dictionary Server)](https://en.wikipedia.org/wiki/Redis) is an open-source in-memory storage,
> used as a distributed, in-memory key–value database, cache and message broker, with optional durability.
> Because it holds all data in memory and because of its design, `Redis` offers low-latency reads and writes,
> making it particularly suitable for use cases that require a cache. Redis is the most popular NoSQL database,
> and one of the most popular databases overall.

This page covers how to use the [Redis](https://redis.com) ecosystem within LangChain.
It is broken into two parts: installation and setup, and then references to specific Redis wrappers.

## [​](#installation-and-setup) Installation and setup

Install the Python SDK and LangChain Redis integration:

pip

uv

Copy

```
pip install redis langchain-redis
```

To run Redis locally, you can use Docker:

Copy

```
docker run --name langchain-redis -d -p 6379:6379 redis redis-server --save 60 1 --loglevel warning
```

To stop the container:

Copy

```
docker stop langchain-redis
```

And to start it again:

Copy

```
docker start langchain-redis
```

### [​](#connections) Connections

We need a redis url connection string to connect to the database support either a stand alone Redis server
or a High-Availability setup with Replication and Redis Sentinels.

#### [​](#redis-standalone-connection-url) Redis standalone connection url

For standalone `Redis` server, the official redis connection url formats can be used as describe in the python redis modules
“from\_url()” method [Redis.from\_url](https://redis-py.readthedocs.io/en/stable/connections.html#redis.Redis.from_url)
Example: `redis_url = "redis://:secret-pass@localhost:6379/0"`

#### [​](#redis-sentinel-connection-url) Redis sentinel connection url

For [Redis sentinel setups](https://redis.io/docs/management/sentinel/) the connection scheme is “redis+sentinel”.
This is an unofficial extensions to the official IANA registered protocol schemes as long as there is no connection url
for Sentinels available.
Example: `redis_url = "redis+sentinel://:secret-pass@sentinel-host:26379/mymaster/0"`
The format is `redis+sentinel://$USERNAME:$PASSWORD@$HOST_OR_IP:$PORT/$SERVICE_NAME/$DB_NUMBER`
with the default values of “service-name = mymaster” and “db-number = 0” if not set explicit.
The service-name is the redis server monitoring group name as configured within the Sentinel.
The current url format limits the connection string to one sentinel host only (no list can be given) and
both Redis server and sentinel must have the same password set (if used).

#### [​](#redis-cluster-connection-url) Redis cluster connection url

Redis cluster is not supported right now for all methods requiring a “redis\_url” parameter.
The only way to use a Redis Cluster is with LangChain classes accepting a preconfigured Redis client like `RedisCache`
(example below).

## [​](#cache) Cache

The Cache wrapper allows for [Redis](https://redis.io) to be used as a remote, low-latency, in-memory cache for LLM prompts and responses.

### [​](#standard-cache) Standard cache

The standard cache is the Redis bread & butter of use case in production for both [open-source](https://redis.io) and [enterprise](https://redis.com) users globally.

Copy

```
from langchain_redis import RedisCache
```

To use this cache with your LLMs:

Copy

```
from langchain.globals import set_llm_cache
import redis

redis_client = redis.Redis.from_url(...)
set_llm_cache(RedisCache(redis_client))
```

### [​](#semantic-cache) Semantic cache

Semantic caching allows users to retrieve cached prompts based on semantic similarity between the user input and previously cached results. Under the hood it blends Redis as both a cache and a vectorstore.

Copy

```
from langchain_redis import RedisSemanticCache
```

To use this cache with your LLMs:

Copy

```
from langchain.globals import set_llm_cache
import redis

# use any embedding provider...
from tests.integration_tests.vectorstores.fake_embeddings import FakeEmbeddings

redis_url = "redis://localhost:6379"

set_llm_cache(RedisSemanticCache(
    embedding=FakeEmbeddings(),
    redis_url=redis_url
))
```

## [​](#vectorstore) VectorStore

The vectorstore wrapper turns Redis into a low-latency [vector database](https://redis.com/solutions/use-cases/vector-database/) for semantic search or LLM content retrieval.

Copy

```
from langchain_community.vectorstores import Redis
```

## [​](#retriever) Retriever

The Redis vector store retriever wrapper generalizes the vectorstore class to perform
low-latency document retrieval. To create the retriever, simply
call `.as_retriever()` on the base vectorstore class.

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/providers/redis.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.