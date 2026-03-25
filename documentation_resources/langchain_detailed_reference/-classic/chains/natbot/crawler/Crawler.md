<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/natbot/crawler/Crawler -->

Classv1.2.13 (latest)●Since v1.0

# Crawler

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
```


```
Crawler(
    self,
)
```

## Constructors

[constructor

\_\_init\_\_](/python/langchain-classic/chains/natbot/crawler/Crawler/__init__)

## Attributes

[attribute

browser: Browser](/python/langchain-classic/chains/natbot/crawler/Crawler/browser)[attribute

page: Page](/python/langchain-classic/chains/natbot/crawler/Crawler/page)[attribute

page\_element\_buffer: dict[int, ElementInViewPort]](/python/langchain-classic/chains/natbot/crawler/Crawler/page_element_buffer)[attribute

client: CDPSession](/python/langchain-classic/chains/natbot/crawler/Crawler/client)

## Methods

[method

go\_to\_page

Navigate to the given URL.](/python/langchain-classic/chains/natbot/crawler/Crawler/go_to_page)[method

scroll

Scroll the page in the given direction.](/python/langchain-classic/chains/natbot/crawler/Crawler/scroll)[method

click

Click on an element with the given id.](/python/langchain-classic/chains/natbot/crawler/Crawler/click)[method

type

Type text into an element with the given id.](/python/langchain-classic/chains/natbot/crawler/Crawler/type)[method

enter

Press the Enter key.](/python/langchain-classic/chains/natbot/crawler/Crawler/enter)[method

crawl

Crawl the current page.](/python/langchain-classic/chains/natbot/crawler/Crawler/crawl)


