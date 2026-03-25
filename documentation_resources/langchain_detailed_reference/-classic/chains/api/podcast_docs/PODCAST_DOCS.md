<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/api/podcast_docs/PODCAST_DOCS -->

Attributev1.2.13 (latest)●Since v1.0

# PODCAST\_DOCS


```
PODCAST_DOCS = 'API documentation:\nEndpoint: https://listen-api.listennotes.com/api/v2\nGET /search\n\nThis API is for searching podcasts or episodes.\n\nQuery parameters table:\nq | string | Search term, e.g., person, place, topic... You can use double quotes to do verbatim match, e.g., "game of thrones". Otherwise, it\'s fuzzy search. | required\ntype | string | What type of contents do you want to search for? Available values: episode, podcast, curated. default: episode | optional\npage_size | integer | The maximum number of search results per page. A valid value should be an integer between 1 and 10 (
  inclusive). default: 3 | optional\nlanguage | string | Limit search results to a specific language, e.g., English, Chinese ... If not specified, it\'ll be any language. It works only when type is episode or podcast. | optional\nregion | string | Limit search results to a specific region (e.g.,
  us,
  gb,
  in...). If not specified, it\'ll be any region. It works only when type is episode or podcast. | optional\nlen_min | integer | Minimum audio length in minutes. Applicable only when type parameter is episode or podcast. If type parameter is episode, it\'s for audio length of an episode. If type parameter is podcast, it\'s for average audio length of all episodes in a podcast. | optional\nlen_max | integer | Maximum audio length in minutes. Applicable only when type parameter is episode or podcast. If type parameter is episode, it\'s for audio length of an episode. If type parameter is podcast, it\'s for average audio length of all episodes in a podcast. | optional\n\nResponse schema (JSON object):\nnext_offset | integer | optional\ntotal | integer | optional\nresults | array[object] (Episode / Podcast List Result Object
)\n\nEach object in the "results" key has the following schema:\nlistennotes_url | string | optional\nid | integer | optional\ntitle_highlighted | string | optional\n\nUse page_size: 3\n'
```


