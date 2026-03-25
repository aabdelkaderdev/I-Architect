<!-- Source: https://docs.streamlit.io/develop/api-reference/caching-and-state/st.query_params -->

Show API reference for

Version v1.55.0*expand\_more*

`st.query_params` provides a dictionary-like interface to access query parameters in your app's URL and is available as of Streamlit 1.30.0. It behaves similarly to `st.session_state` with the notable exception that keys may be repeated in an app's URL. Handling of repeated keys requires special consideration as explained below.

`st.query_params` can be used with both key and attribute notation. For example, `st.query_params.my_key` and `st.query_params["my_key"]`. All keys and values will be set and returned as strings. When you write to `st.query_params`, key-value pair prefixed with `?` is added to the end of your app's URL. Each additional pair is prefixed with `&` instead of `?`. Query parameters are cleared when navigating between pages in a multipage app.

For example, consider the following URL:

```
https://your_app.streamlit.app/?first_key=1&second_key=two&third_key=true
```

The parameters in the URL above will be accessible in `st.query_params` as:

```
{
    "first_key" : "1",
    "second_key" : "two",
    "third_key" : "true"
}
```

This means you can use those parameters in your app like this:

```
# You can read query params using key notation
if st.query_params["first_key"] == "1":
    do_something()

# ...or using attribute notation
if st.query_params.second_key == "two":
    do_something_else()

# And you can change a param by just writing to it
st.query_params.first_key = 2  # This gets converted to str automatically
```

When a key is repeated in your app's URL (`?a=1&a=2&a=3`), dict-like methods will return only the last value. In this example, `st.query_params["a"]` returns `"3"`. To get all keys as a list, use the [`.get_all()`](/develop/api-reference/caching-and-state/st.query_params#stquery_paramsget_all) method shown below. To set the value of a repeated key, assign the values as a list. For example, `st.query_params.a = ["1", "2", "3"]` produces the repeated key given at the beginning of this paragraph.

`st.query_params` can't get or set embedding settings as described in [Embed your app](/deploy/streamlit-community-cloud/share-your-app/embed-your-app#embed-options). `st.query_params.embed` and `st.query_params.embed_options` will raise an `AttributeError` or `StreamlitAPIException` when trying to get or set their values, respectively.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/runtime/state/query_params_proxy.py#L135 "View st.clear source code on GitHub") | |
| --- | --- |
| st.query\_params.clear() | |
|  |  |
| --- | --- |
| Returns | |
| (None) | No description |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/runtime/state/query_params_proxy.py#L175 "View st.from_dict source code on GitHub") | |
| --- | --- |
| st.query\_params.from\_dict(params) | |
| Parameters | |
| params (dict) | A dictionary used to replace the current query parameters. |

#### Example

```
import streamlit as st

st.query_params.from_dict({"foo": "bar", "baz": [1, "two"]})
```

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/runtime/state/query_params_proxy.py#L112 "View st.get_all source code on GitHub") | |
| --- | --- |
| st.query\_params.get\_all(key) | |
| Parameters | |
| key (str) | The label of the query parameter in the URL. |
|  |  |
| --- | --- |
| Returns | |
| (List[str]) | A list of values associated to the given key. May return zero, one, or multiple values. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/runtime/state/query_params_proxy.py#L147 "View st.to_dict source code on GitHub") | |
| --- | --- |
| st.query\_params.to\_dict() | |
|  |  |
| --- | --- |
| Returns | |
| (Dict[str,str]) | A dictionary of the current query parameters in the app's URL. |

[*arrow\_back*Previous: st.context](/develop/api-reference/caching-and-state/st.context)[*arrow\_forward*Next: st.experimental\_get\_query\_params](/develop/api-reference/caching-and-state/st.experimental_get_query_params)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI