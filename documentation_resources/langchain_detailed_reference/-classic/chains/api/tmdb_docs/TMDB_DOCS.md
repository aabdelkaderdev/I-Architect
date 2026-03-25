<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/api/tmdb_docs/TMDB_DOCS -->

Attributev1.2.13 (latest)●Since v1.0

# TMDB\_DOCS


```
TMDB_DOCS = 'API documentation:\nEndpoint: https://api.themoviedb.org/3\nGET /search/movie\n\nThis API is for searching movies.\n\nQuery parameters table:\nlanguage | string | Pass a ISO 639-1 value to display translated data for the fields that support it. minLength: 2, pattern: (
  [a-z]{2})-([A-Z]{2}), default: en-US | optional\nquery | string | Pass a text query to search. This value should be URI encoded. minLength: 1 | required\npage | integer | Specify which page to query. minimum: 1, maximum: 1000, default: 1 | optional\ninclude_adult | boolean | Choose whether to include adult (pornography) content in the results. default | optional\nregion | string | Specify a ISO 3166-1 code to filter release dates. Must be uppercase. pattern: ^[A-Z]{2}$ | optional\nyear | integer  | optional\nprimary_release_year | integer | optional\n\nResponse schema (JSON object):\npage | integer | optional\ntotal_results | integer | optional\ntotal_pages | integer | optional\nresults | array[object] (Movie List Result Object
)\n\nEach object in the "results" key has the following schema:\nposter_path | string or null | optional\nadult | boolean | optional\noverview | string | optional\nrelease_date | string | optional\ngenre_ids | array[integer] | optional\nid | integer | optional\noriginal_title | string | optional\noriginal_language | string | optional\ntitle | string | optional\nbackdrop_path | string or null | optional\npopularity | number | optional\nvote_count | integer | optional\nvideo | boolean | optional\nvote_average | number | optional'
```


