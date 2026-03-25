<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/natbot/crawler -->

Modulev1.2.13 (latest)●Since v1.0

# crawler

## Attributes

[attribute

logger](/python/langchain-classic/chains/natbot/crawler/logger)[attribute

black\_listed\_elements: set[str]](/python/langchain-classic/chains/natbot/crawler/black_listed_elements)

## Classes

[class

ElementInViewPort

A typed dictionary containing information about elements in the viewport.](/python/langchain-classic/chains/natbot/crawler/ElementInViewPort)[class

Crawler

A crawler for web pages.

**Security Note**: This is an implementation of a crawler that uses a browser via
Playwright.

```
This crawler can be used to load arbitrary webpages INCLUDING content
from the local file system.

Control access to who can submit crawling requests and what network access
the crawler has.

Make sure to scope permissions to the minimal permissions necessary for
the application.

See https://docs.langchain.com/oss/python/security-policy for more information.
```](/python/langchain-classic/chains/natbot/crawler/Crawler)


