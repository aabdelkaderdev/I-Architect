<!-- Source: https://docs.streamlit.io/develop/api-reference/caching-and-state/st.cache_resource -->

Show API reference for

Version v1.55.0*expand\_more*

This page only contains information on the `st.cache_resource` API. For a deeper dive into caching and how to use it, check out [Caching](/develop/concepts/architecture/caching).

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/runtime/caching/cache_resource_api.py#L352 "View st.cache_resource source code on GitHub") | |
| --- | --- |
| st.cache\_resource(func, \*, ttl, max\_entries, show\_spinner, show\_time=False, validate, hash\_funcs=None, on\_release=None, scope="global") | |
| Parameters | |
| func (callable) | The function that creates the cached resource. Streamlit hashes the function's source code. |
| ttl (float, timedelta, str, or None) | The maximum age of a returned entry from the cache. This can be one of the following values:   - None if cache entries should never expire (default). - A number specifying the time in seconds. - A string specifying the time in a format supported by [Pandas's   Timedelta constructor](https://pandas.pydata.org/docs/reference/api/pandas.Timedelta.html),   e.g. "1d", "1.5 days", or "1h23s". Note that number strings   without units are treated by Pandas as nanoseconds. - A timedelta object from [Python's built-in datetime library](https://docs.python.org/3/library/datetime.html#timedelta-objects),   e.g. timedelta(days=1).   Changes to this value will trigger a new cache to be created. |
| max\_entries (int or None) | The maximum number of entries to keep in the cache, or None for an unbounded cache. When a new entry is added to a full cache, the oldest cached entry will be removed. Defaults to None.  Changes to this value will trigger a new cache to be created. |
| show\_spinner (bool or str) | Enable the spinner. Default is True to show a spinner when there is a "cache miss" and the cached resource is being created. If string, value of show\_spinner param will be used for spinner text. |
| show\_time (bool) | Whether to show the elapsed time next to the spinner text. If this is False (default), no time is displayed. If this is True, elapsed time is displayed with a precision of 0.1 seconds. The time format is not configurable. |
| validate (callable or None) | An optional validation function for cached resources. validate is called each time the cached value is accessed. It receives the cached value as its only parameter and it must return a boolean. If validate returns False, the current cached value is discarded, and the decorated function is called to compute a new value. This is useful e.g. to check the health of database connections. |
| hash\_funcs (dict or None) | Mapping of types or fully qualified names to hash functions. This is used to override the behavior of the hasher inside Streamlit's caching mechanism: when the hasher encounters an object, it will first check to see if its type matches a key in this dict and, if so, will use the provided function to generate a hash for it. See below for an example of how this can be used. |
| on\_release (callable or None) | A function to call when an entry is removed from the cache. The removed item will be provided to the function as an argument.  This is only useful for caches that remove entries normally. Most commonly, this is used session-scoped caches to release per-session resources. This can also be used with max\_entries or ttl settings.  TTL expiration only happens when expired resources are accessed. Therefore, don't rely on TTL expiration to guarantee timely cleanup. Also, expiration can happen on any script run. Ensure that on\_release functions are thread-safe and don't rely on session state.  The on\_release function isn't guaranteed to be called when an app is shut down. |
| scope ("global" or "session") | The scope for the resource cache. If this is "global" (default), the resource is cached globally. If this is "session", the resource is removed from the cache when the session disconnects.  Because a session-scoped cache is cleared when a session disconnects, an unstable network connection can cause the cache to populate multiple times in a single session. If this is a problem, you might consider adjusting the server.websocketPingInterval configuration option. |

#### Example

**Example 1: Global cache**

By default, an @st.cache\_resource-decorated function uses a global cache.

```
import streamlit as st

@st.cache_resource
def get_database_session(url):
    # Create a database session object that points to the URL.
    return session

s1 = get_database_session(SESSION_URL_1)
# Actually executes the function, since this is the first time it was
# encountered.

s2 = get_database_session(SESSION_URL_1)
# Does not execute the function. Instead, returns its previously computed
# value. This means that now the connection object in s1 is the same as in s2.

s3 = get_database_session(SESSION_URL_2)
# This is a different URL, so the function executes.
```

**Example 2: Session-scoped cache**

By passing scope="session", an @st.cache\_resource-decorated function
uses a session-scoped cache. You can also use on\_release to clean up
resources when they are no longer needed.

```
import streamlit as st

@st.cache_resource(scope="session", on_release=lambda sess: sess.close())
def get_database_session(url):
    # Create a database session object that points to the URL.
    return session
```

**Example 3: Unhashable arguments**

By default, all parameters to a cached function must be hashable.
Any parameter whose name begins with \_ will not be hashed. You can use
this as an "escape hatch" for parameters that are not hashable:

```
import streamlit as st

@st.cache_resource
def get_database_session(_sessionmaker, url):
    # Create a database connection object that points to the URL.
    return connection

s1 = get_database_session(create_sessionmaker(), DATA_URL_1)
# Actually executes the function, since this is the first time it was
# encountered.

s2 = get_database_session(create_sessionmaker(), DATA_URL_1)
# Does not execute the function. Instead, returns its previously computed
# value - even though the _sessionmaker parameter was different
# in both calls.
```

**Example 4: Clearing a cache**

A cached function's cache can be procedurally cleared:

```
import streamlit as st

@st.cache_resource
def get_database_session(_sessionmaker, url):
    # Create a database connection object that points to the URL.
    return connection

get_database_session.clear(_sessionmaker, "https://streamlit.io/")
# Clear the cached entry for the arguments provided.

get_database_session.clear()
# Clear all cached entries for this function.
```

**Example 5: Custom hashing**

To override the default hashing behavior, pass a custom hash function.
You can do that by mapping a type (e.g. Person) to a hash
function (str) like this:

```
import streamlit as st
from pydantic import BaseModel

class Person(BaseModel):
    name: str

@st.cache_resource(hash_funcs={Person: str})
def get_person_name(person: Person):
    return person.name
```

Alternatively, you can map the type's fully-qualified name
(e.g. "\_\_main\_\_.Person") to the hash function instead:

```
import streamlit as st
from pydantic import BaseModel

class Person(BaseModel):
    name: str

@st.cache_resource(hash_funcs={"__main__.Person": str})
def get_person_name(person: Person):
    return person.name
```

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/runtime/caching/cache_resource_api.py#L631 "View st.cache_resource.clear source code on GitHub") | |
| --- | --- |
| st.cache\_resource.clear() | |

#### Example

In the example below, pressing the "Clear All" button will clear *all* cache\_resource caches. i.e. Clears cached global resources from all functions decorated with `@st.cache_resource`.

```
import streamlit as st
from transformers import BertModel

@st.cache_resource
 def get_database_session(url):
     # Create a database session object that points to the URL.
     return session

@st.cache_resource
def get_model(model_type):
    # Create a model of the specified type.
    return BertModel.from_pretrained(model_type)

if st.button("Clear All"):
    # Clears all st.cache_resource caches:
    st.cache_resource.clear()
```

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/runtime/caching/cache_utils.py#L423 "View st.clear source code on GitHub") | |
| --- | --- |
| CachedFunc.clear(\*args, \*\*kwargs) | |
| Parameters | |
| \*args (Any) | Arguments of the cached functions. |
| \*\*kwargs (Any) | Keyword arguments of the cached function. |

#### Example

```
import streamlit as st
import time

@st.cache_data
def foo(bar):
    time.sleep(2)
    st.write(f"Executed foo({bar}).")
    return bar

if st.button("Clear all cached values for `foo`", on_click=foo.clear):
    foo.clear()

if st.button("Clear the cached value of `foo(1)`"):
    foo.clear(1)

foo(1)
foo(2)
```

Since version 1.16.0, cached functions can contain Streamlit commands! For example, you can do this:

```
from transformers import pipeline

@st.cache_resource
def load_model():
    model = pipeline("sentiment-analysis")
    st.success("Loaded NLP model from Hugging Face!")  # 👈 Show a success message
    return model
```

As we know, Streamlit only runs this function if it hasn’t been cached before. On this first run, the `st.success` message will appear in the app. But what happens on subsequent runs? It still shows up! Streamlit realizes that there is an `st.` command inside the cached function, saves it during the first run, and replays it on subsequent runs. Replaying static elements works for both caching decorators.

You can also use this functionality to cache entire parts of your UI:

```
@st.cache_resource
def load_model():
    st.header("Data analysis")
    model = torchvision.models.resnet50(weights=ResNet50_Weights.DEFAULT)
    st.success("Loaded model!")
    st.write("Turning on evaluation mode...")
    model.eval()
    st.write("Here's the model:")
    return model
```

You can also use [interactive input widgets](/develop/api-reference/widgets) like `st.slider` or `st.text_input` in cached functions. Widget replay is an experimental feature at the moment. To enable it, you need to set the `experimental_allow_widgets` parameter:

```
@st.cache_resource(experimental_allow_widgets=True)  # 👈 Set the parameter
def load_model():
    pretrained = st.checkbox("Use pre-trained model:")  # 👈 Add a checkbox
    model = torchvision.models.resnet50(weights=ResNet50_Weights.DEFAULT, pretrained=pretrained)
    return model
```

Streamlit treats the checkbox like an additional input parameter to the cached function. If you uncheck it, Streamlit will see if it has already cached the function for this checkbox state. If yes, it will return the cached value. If not, it will rerun the function using the new slider value.

Using widgets in cached functions is extremely powerful because it lets you cache entire parts of your app. But it can be dangerous! Since Streamlit treats the widget value as an additional input parameter, it can easily lead to excessive memory usage. Imagine your cached function has five sliders and returns a 100 MB DataFrame. Then we’ll add 100 MB to the cache for *every permutation* of these five slider values – even if the sliders do not influence the returned data! These additions can make your cache explode very quickly. Please be aware of this limitation if you use widgets in cached functions. We recommend using this feature only for isolated parts of your UI where the widgets directly influence the cached return value.

Support for widgets in cached functions is currently experimental. We may change or remove it anytime without warning. Please use it with care!

Two widgets are currently not supported in cached functions: `st.file_uploader` and `st.camera_input`. We may support them in the future. Feel free to [open a GitHub issue](https://github.com/streamlit/streamlit/issues) if you need them!

[*arrow\_back*Previous: st.cache\_data](/develop/api-reference/caching-and-state/st.cache_data)[*arrow\_forward*Next: st.experimental\_memo](/develop/api-reference/caching-and-state/st.experimental_memo)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI