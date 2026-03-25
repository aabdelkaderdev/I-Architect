<!-- Source: https://docs.streamlit.io/develop/api-reference/caching-and-state -->

Optimize performance and add statefulness to your app!

Streamlit provides powerful [cache primitives](/develop/concepts/architecture/caching) for data and global resources. They allow your app to stay performant even when loading data from the web, manipulating large datasets, or performing expensive computations.

[#### Cache data

Function decorator to cache functions that return data (e.g. dataframe transforms, database queries, ML inference).

```
@st.cache_data
def long_function(param1, param2):
  # Perform expensive computation here or
  # fetch data from the web here
  return data
```](/develop/api-reference/caching-and-state/st.cache_data)[#### Cache resource

Function decorator to cache functions that return global resources (e.g. database connections, ML models).

```
@st.cache_resource
def init_model():
  # Return a global resource here
  return pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
  )
```](/develop/api-reference/caching-and-state/st.cache_resource)

Streamlit re-executes your script with each user interaction. Widgets have built-in statefulness between reruns, but Session State lets you do more!

[#### Context

`st.context` provides a read-only interface to access cookies, headers, locale, and other browser-session information.

```
st.context.cookies
st.context.headers
```](/develop/api-reference/caching-and-state/st.context)[#### Session State

Save data between reruns and across pages.

```
st.session_state["foo"] = "bar"
```](/develop/api-reference/caching-and-state/st.session_state)[#### Query parameters

Get, set, or clear the query parameters that are shown in the browser's URL bar.

```
st.query_params[key] = value
st.query_params.clear()
```](/develop/api-reference/caching-and-state/st.query_params)

[*arrow\_back*Previous: Execution flow](/develop/api-reference/execution-flow)[*arrow\_forward*Next: st.cache\_data](/develop/api-reference/caching-and-state/st.cache_data)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI