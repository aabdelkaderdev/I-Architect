<!-- Source: https://docs.streamlit.io/develop/api-reference/connections/st.connections.snowparkconnection -->

Show API reference for

Version v1.55.0*expand\_more*

This page only contains the `st.connections.SnowparkConnection` class. For a deeper dive into creating and managing data connections within Streamlit apps, read [Connecting to data](/develop/concepts/connections/connecting-to-data).

| Class description[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/connections/snowpark_connection.py#L49 "View st.SnowparkConnection source code on GitHub") | |
| --- | --- |
| st.connections.SnowparkConnection(connection\_name, \*\*kwargs) | |
|  |  |
| --- | --- |
| Methods | |
| [close](/develop/api-reference/connections/st.connections.snowparkconnection#snowparkconnectionclose)() | A function to invoke when this connection needs to be cleaned up. |
| [query](/develop/api-reference/connections/st.connections.snowparkconnection#snowparkconnectionquery)(sql, ttl=None) | Run a read-only SQL query. |
| [reset](/develop/api-reference/connections/st.connections.snowparkconnection#snowparkconnectionreset)() | Reset this connection so that it gets reinitialized the next time it's used. |
| [safe\_session](/develop/api-reference/connections/st.connections.snowparkconnection#snowparkconnectionsafe_session)() | Grab the underlying Snowpark session in a thread-safe manner. |
| Attributes | |
| [session](/develop/api-reference/connections/st.connections.snowparkconnection#snowparkconnectionsession) | Access the underlying Snowpark session. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/connections/snowpark_connection.py#L110 "View st.query source code on GitHub") | |
| --- | --- |
| SnowparkConnection.query(sql, ttl=None) | |
| Parameters | |
| sql (str) | The read-only SQL query to execute. |
| ttl (float, int, timedelta or None) | The maximum number of seconds to keep results in the cache, or None if cached results should not expire. The default is None. |
|  |  |
| --- | --- |
| Returns | |
| (pandas.DataFrame) | The result of running the query, formatted as a pandas DataFrame. |

#### Example

```
import streamlit as st

conn = st.connection("snowpark")
df = conn.query("SELECT * FROM pet_owners")
st.dataframe(df)
```

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/connections/base_connection.py#L134 "View st.reset source code on GitHub") | |
| --- | --- |
| SnowparkConnection.reset() | |
|  |  |
| --- | --- |
| Returns | |
| (None) | No description |

#### Example

```
import streamlit as st

conn = st.connection("my_conn")

# Reset the connection before using it if it isn't healthy
# Note: is_healthy() isn't a real method and is just shown for example here.
if not conn.is_healthy():
    conn.reset()

# Do stuff with conn...
```

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/connections/snowpark_connection.py#L203 "View st.safe_session source code on GitHub") | |
| --- | --- |
| SnowparkConnection.safe\_session() | |

#### Example

```
import streamlit as st

conn = st.connection("snowpark")
with conn.safe_session() as session:
    df = session.table("mytable").limit(10).to_pandas()

st.dataframe(df)
```

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/connections/snowpark_connection.py#L180 "View st.session source code on GitHub") | |
| --- | --- |
| SnowparkConnection.session | |

#### Example

```
import streamlit as st

session = st.connection("snowpark").session
df = session.table("mytable").limit(10).to_pandas()
st.dataframe(df)
```

[*arrow\_back*Previous: st.experimental\_connection](/develop/api-reference/connections/st.experimental_connection)[*arrow\_forward*Next: ExperimentalBaseConnection](/develop/api-reference/connections/st.connections.experimentalbaseconnection)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI