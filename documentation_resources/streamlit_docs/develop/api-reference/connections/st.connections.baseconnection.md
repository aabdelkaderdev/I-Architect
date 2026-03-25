<!-- Source: https://docs.streamlit.io/develop/api-reference/connections/st.connections.baseconnection -->

Show API reference for

Version v1.55.0*expand\_more*

This page only contains information on the `st.connections.BaseConnection` class. For a deeper dive into creating and managing data connections within Streamlit apps, read [Connecting to data](/develop/concepts/connections/connecting-to-data).

| Class description[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/connections/base_connection.py#L28 "View st.BaseConnection source code on GitHub") | |
| --- | --- |
| st.connections.BaseConnection(connection\_name, \*\*kwargs) | |
|  |  |
| --- | --- |
| Methods | |
| [close](/develop/api-reference/connections/st.connections.baseconnection#baseconnectionclose)() | A function to invoke when this connection needs to be cleaned up. |
| [reset](/develop/api-reference/connections/st.connections.baseconnection#baseconnectionreset)() | Reset this connection so that it gets reinitialized the next time it's used. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/connections/base_connection.py#L134 "View st.reset source code on GitHub") | |
| --- | --- |
| BaseConnection.reset() | |
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

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/connections/base_connection.py#L209 "View st.close source code on GitHub") | |
| --- | --- |
| BaseConnection.close() | |
|  |  |
| --- | --- |
| Returns | |
| (None) | No description |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/connections/base_connection.py#L189 "View st.scope source code on GitHub") | |
| --- | --- |
| BaseConnection.scope(cls) | |
|  |  |
| --- | --- |
| Returns | |
| ("global" or "session") | No description |

[*arrow\_back*Previous: SQLConnection](/develop/api-reference/connections/st.connections.sqlconnection)[*arrow\_forward*Next: st.experimental\_connection](/develop/api-reference/connections/st.experimental_connection)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI