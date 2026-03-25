<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/api/news_docs/NEWS_DOCS -->

Attributev1.2.13 (latest)●Since v1.0

# NEWS\_DOCS


```
NEWS_DOCS = "API documentation:\nEndpoint: https://newsapi.org\nTop headlines /v2/top-headlines\n\nThis endpoint provides live top and breaking headlines for a country, specific category in a country, single source, or multiple sources. You can also search with keywords. Articles are sorted by the earliest date published first.\n\nThis endpoint is great for retrieving headlines for use with news tickers or similar.\nRequest parameters\n\n    country | The 2-letter ISO 3166-1 code of the country you want to get headlines for. Possible options: ae ar at au be bg br ca ch cn co cu cz de eg fr gb gr hk hu id ie il in it jp kr lt lv ma mx my ng nl no nz ph pl pt ro rs ru sa se sg si sk th tr tw ua us ve za. Note: you can't mix this param with the sources param.\n    category | The category you want to get headlines for. Possible options: business entertainment general health science sports technology. Note: you can't mix this param with the sources param.\n    sources | A comma-separated string of identifiers for the news sources or blogs you want headlines from. Use the /top-headlines/sources endpoint to locate these programmatically or look at the sources index. Note: you can't mix this param with the country or category params.\n    q | Keywords or a phrase to search for.\n    pageSize | int | The number of results to return per page (
  request). 20 is the default, 100 is the maximum.\n    page | int | Use this to page through the results if the total results found is greater than the page size.\n\nResponse object\n    status | string | If the request was successful or not. Options: ok, error. In the case of error a code and message property will be populated.\n    totalResults | int | The total number of results available for your request.\n    articles | array[article] | The results of the request.\n    source | object | The identifier id and a display name name for the source this article came from.\n    author | string | The author of the article\n    title | string | The headline or title of the article.\n    description | string | A description or snippet from the article.\n    url | string | The direct URL to the article.\n    urlToImage | string | The URL to a relevant image for the article.\n    publishedAt | string | The date and time that the article was published, in UTC (+000
)\n    content | string | The unformatted content of the article, where available. This is truncated to 200 chars.\n\nUse page size: 2\n"
```


