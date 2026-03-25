<!-- Source: https://docs.streamlit.io/develop/api-reference/connections/st.connections.sqlconnection -->

Show API reference for

Version v1.55.0*expand\_more*

This page only contains the `st.connections.SQLConnection` class. For a deeper dive into creating and managing data connections within Streamlit apps, read [Connecting to data](/develop/concepts/connections/connecting-to-data).

| Class description[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/connections/sql_connection.py#L55 "View st.SQLConnection source code on GitHub") | |
| --- | --- |
| st.connections.SQLConnection(connection\_name, \*\*kwargs) | |
|  |  |
| --- | --- |
| Methods | |
| [close](/develop/api-reference/connections/st.connections.sqlconnection#sqlconnectionclose)() | A function to invoke when this connection needs to be cleaned up. |
| [connect](/develop/api-reference/connections/st.connections.sqlconnection#sqlconnectionconnect)() | Call .connect() on the underlying SQLAlchemy Engine, returning a new connection object. |
| [query](/develop/api-reference/connections/st.connections.sqlconnection#sqlconnectionquery)(sql, \*, show\_spinner="Running `sql.query(...)`.", ttl=None, index\_col=None, chunksize=None, params=None, \*\*kwargs) | Run a read-only query. |
| [reset](/develop/api-reference/connections/st.connections.sqlconnection#sqlconnectionreset)() | Reset this connection so that it gets reinitialized the next time it's used. |
| Attributes | |
| [driver](/develop/api-reference/connections/st.connections.sqlconnection#sqlconnectiondriver) | The name of the driver used by the underlying SQLAlchemy Engine. |
| [engine](/develop/api-reference/connections/st.connections.sqlconnection#sqlconnectionengine) | The underlying SQLAlchemy Engine. |
| [session](/develop/api-reference/connections/st.connections.sqlconnection#sqlconnectionsession) | Return a SQLAlchemy Session. |

#### Examples

**Example 1: Configuration with URL**

You can configure your SQL connection using Streamlit's
[Secrets management](https://docs.streamlit.io/develop/concepts/connections/secrets-management).
The following example specifies a SQL connection URL.

.streamlit/secrets.toml:

```
[connections.sql]
url = "xxx+xxx://xxx:xxx@xxx:xxx/xxx"
```

Your app code:

```
import streamlit as st

conn = st.connection("sql")
df = conn.query("SELECT * FROM pet_owners")
st.dataframe(df)
```

**Example 2: Configuration with dialect, host, and username**

If you do not specify url, you must at least specify dialect,
host, and username instead. The following example also includes
password.

.streamlit/secrets.toml:

```
[connections.sql]
dialect = "xxx"
host = "xxx"
username = "xxx"
password = "xxx"
```

Your app code:

```
import streamlit as st

conn = st.connection("sql")
df = conn.query("SELECT * FROM pet_owners")
st.dataframe(df)
```

**Example 3: Configuration with keyword arguments**

You can configure your SQL connection with keyword arguments (with or
without secrets.toml). For example, if you use Microsoft Entra ID with
a Microsoft Azure SQL server, you can quickly set up a local connection for
development using [interactive authentication](https://learn.microsoft.com/en-us/sql/connect/odbc/using-azure-active-directory?view=sql-server-ver16#new-andor-modified-dsn-and-connection-string-keywords).

This example requires the [Microsoft ODBC Driver for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/microsoft-odbc-driver-for-sql-server?view=sql-server-ver16)
for *Windows* in addition to the sqlalchemy and pyodbc packages for
Python.

```
import streamlit as st

conn = st.connection(
    "sql",
    dialect="mssql",
    driver="pyodbc",
    host="xxx.database.windows.net",
    database="xxx",
    username="xxx",
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "authentication": "ActiveDirectoryInteractive",
        "encrypt": "yes",
    },
)

df = conn.query("SELECT * FROM pet_owners")
st.dataframe(df)
```

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/connections/sql_connection.py#L360 "View st.connect source code on GitHub") | |
| --- | --- |
| SQLConnection.connect() | |
|  |  |
| --- | --- |
| Returns | |
| (sqlalchemy.engine.Connection) | A new SQLAlchemy connection object. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/connections/sql_connection.py#L224 "View st.query source code on GitHub") | |
| --- | --- |
| SQLConnection.query(sql, \*, show\_spinner="Running `sql.query(...)`.", ttl=None, index\_col=None, chunksize=None, params=None, \*\*kwargs) | |
| Parameters | |
| sql (str) | The read-only SQL query to execute. |
| show\_spinner (boolean or string) | Enable the spinner. The default is to show a spinner when there is a "cache miss" and the cached resource is being created. If a string, the value of the show\_spinner param will be used for the spinner text. |
| ttl (float, int, timedelta or None) | The maximum number of seconds to keep results in the cache, or None if cached results should not expire. The default is None. |
| index\_col (str, list of str, or None) | Column(s) to set as index(MultiIndex). Default is None. |
| chunksize (int or None) | If specified, return an iterator where chunksize is the number of rows to include in each chunk. Default is None. |
| params (list, tuple, dict or None) | List of parameters to pass to the execute method. The syntax used to pass parameters is database driver dependent. Check your database driver documentation for which of the five syntax styles, described in [PEP 249 paramstyle](https://peps.python.org/pep-0249/#paramstyle), is supported. Default is None. |
| \*\*kwargs (dict) | Additional keyword arguments are passed to [pandas.read\_sql](https://pandas.pydata.org/docs/reference/api/pandas.read_sql.html). |
|  |  |
| --- | --- |
| Returns | |
| (pandas.DataFrame) | The result of running the query, formatted as a pandas DataFrame. |

#### Example

```
import streamlit as st

conn = st.connection("sql")
df = conn.query(
    "SELECT * FROM pet_owners WHERE owner = :owner",
    ttl=3600,
    params={"owner": "barbara"},
)
st.dataframe(df)
```

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/connections/base_connection.py#L134 "View st.reset source code on GitHub") | |
| --- | --- |
| SQLConnection.reset() | |
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

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/connections/sql_connection.py#L389 "View st.driver source code on GitHub") | |
| --- | --- |
| SQLConnection.driver | |
|  |  |
| --- | --- |
| Returns | |
| (str) | The name of the driver. For example, "pyodbc" or "psycopg2". |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/connections/sql_connection.py#L376 "View st.engine source code on GitHub") | |
| --- | --- |
| SQLConnection.engine | |
|  |  |
| --- | --- |
| Returns | |
| (sqlalchemy.engine.base.Engine) | The underlying SQLAlchemy Engine. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/connections/sql_connection.py#L402 "View st.session source code on GitHub") | |
| --- | --- |
| SQLConnection.session | |
|  |  |
| --- | --- |
| Returns | |
| (sqlalchemy.orm.Session) | A SQLAlchemy Session. |

#### Example

```
import streamlit as st
conn = st.connection("sql")
n = st.slider("Pick a number")
if st.button("Add the number!"):
    with conn.session as session:
        session.execute("INSERT INTO numbers (val) VALUES (:n);", {"n": n})
        session.commit()
```

[*arrow\_back*Previous: SnowflakeConnection](/develop/api-reference/connections/st.connections.snowflakeconnection)[*arrow\_forward*Next: BaseConnection](/develop/api-reference/connections/st.connections.baseconnection)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI