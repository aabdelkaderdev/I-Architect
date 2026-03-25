<!-- Source: https://docs.streamlit.io/develop/api-reference/connections/st.connections.snowflakeconnection -->

Show API reference for

Version v1.55.0*expand\_more*

This page only contains the `st.connections.SnowflakeConnection` class. For a deeper dive into creating and managing data connections within Streamlit apps, see [Connect Streamlit to Snowflake](/develop/tutorials/databases/snowflake) and [Connecting to data](/develop/concepts/connections/connecting-to-data).

| Class description[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/connections/snowflake_connection.py#L365 "View st.SnowflakeConnection source code on GitHub") | |
| --- | --- |
| st.connections.SnowflakeConnection(connection\_name, \*\*kwargs) | |
|  |  |
| --- | --- |
| Methods | |
| [close](/develop/api-reference/connections/st.connections.snowflakeconnection#snowflakeconnectionclose)() | Closes the underlying Snowflake connection. |
| [cursor](/develop/api-reference/connections/st.connections.snowflakeconnection#snowflakeconnectioncursor)() | Create a new cursor object from this connection. |
| [query](/develop/api-reference/connections/st.connections.snowflakeconnection#snowflakeconnectionquery)(sql, \*, ttl=None, show\_spinner="Running `snowflake.query(...)`.", params=None, \*\*kwargs) | Run a read-only SQL query. |
| [reset](/develop/api-reference/connections/st.connections.snowflakeconnection#snowflakeconnectionreset)() | Reset this connection so that it gets reinitialized the next time it's used. |
| [session](/develop/api-reference/connections/st.connections.snowflakeconnection#snowflakeconnectionsession)() | Create a new Snowpark session from this connection. |
| [write\_pandas](/develop/api-reference/connections/st.connections.snowflakeconnection#snowflakeconnectionwrite_pandas)(df, table\_name, database=None, schema=None, chunk\_size=None, \*\*kwargs) | Write a pandas.DataFrame to a table in a Snowflake database. |
| Attributes | |
| [raw\_connection](/develop/api-reference/connections/st.connections.snowflakeconnection#snowflakeconnectionraw_connection) | Access the underlying connection object from the Snowflake Connector for Python. |

#### Examples

**Example 1: Configuration with Streamlit secrets**

You can configure your Snowflake connection using Streamlit's
[Secrets management](https://docs.streamlit.io/develop/concepts/connections/secrets-management).
For example, if you have MFA enabled on your account, you can connect using
[key-pair authentication](https://docs.snowflake.com/en/user-guide/key-pair-auth).

```
[connections.snowflake]
account = "xxx-xxx"
user = "xxx"
private_key_file = "/xxx/xxx/xxx.p8"
role = "xxx"
warehouse = "xxx"
database = "xxx"
schema = "xxx"
```

```
import streamlit as st

conn = st.connection("snowflake")
df = conn.query("SELECT * FROM my_table")
```

**Example 2: Configuration with keyword arguments and external authentication**

You can configure your Snowflake connection with keyword arguments. The
keyword arguments are merged with (and take precedence over) the values in
secrets.toml. However, if you name your connection "snowflake" and
don't have a [connections.snowflake] dictionary in your
secrets.toml file, Streamlit will ignore any keyword arguments and use
the default Snowflake connection as described in Example 5 and Example 6.
To configure your connection using only keyword arguments, declare a name
for the connection other than "snowflake".

For example, if your Snowflake account supports SSO, you can set up a quick
local connection for development using [browser-based SSO](https://docs.snowflake.com/en/user-guide/admin-security-fed-auth-use#how-browser-based-sso-works).
Because there is nothing configured in secrets.toml, the name is an
empty string and the type is set to "snowflake". This prevents
Streamlit from ignoring the keyword arguments and using a default
Snowflake connection.

```
import streamlit as st

conn = st.connection(
    "",
    type="snowflake",
    account="xxx-xxx",
    user="xxx",
    authenticator="externalbrowser",
)
df = conn.query("SELECT * FROM my_table")
```

**Example 3: Named connection with Snowflake's connection configuration file**

Snowflake's Python Connector supports a [connection configuration file](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-connect#connecting-using-the-connections-toml-file),
which is well integrated with Streamlit's SnowflakeConnection. If you
already have one or more connections configured, all you need to do is pass
the name of the connection to use.

```
[my_connection]
account = "xxx-xxx"
user = "xxx"
password = "xxx"
warehouse = "xxx"
database = "xxx"
schema = "xxx"
```

```
import streamlit as st

conn = st.connection("my_connection", type="snowflake")
df = conn.query("SELECT * FROM my_table")
```

**Example 4: Named connection with Streamlit secrets and Snowflake's connection configuration file**

If you have a Snowflake configuration file with a connection named
my\_connection as in Example 3, you can pass the connection name through
secrets.toml.

```
[connections.snowflake]
connection_name = "my_connection"
```

```
import streamlit as st

conn = st.connection("snowflake")
df = conn.query("SELECT * FROM my_table")
```

**Example 5: Default connection with an environment variable**

If you don't have a [connections.snowflake] dictionary in your
secrets.toml file and use st.connection("snowflake"), Streamlit
will use the default connection for the [Snowflake Python Connector](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-connect#setting-a-default-connection).

If you have a Snowflake configuration file with a connection named
my\_connection as in Example 3, you can set an environment variable to
declare it as the default Snowflake connection.

```
SNOWFLAKE_DEFAULT_CONNECTION_NAME = "my_connection"
```

```
import streamlit as st

conn = st.connection("snowflake")
df = conn.query("SELECT * FROM my_table")
```

**Example 6: Default connection in Snowflake's connection configuration file**

If you have a Snowflake configuration file that defines your default
connection, Streamlit will automatically use it if no other connection is
declared.

```
[default]
account = "xxx-xxx"
user = "xxx"
password = "xxx"
warehouse = "xxx"
database = "xxx"
schema = "xxx"
```

```
import streamlit as st

conn = st.connection("snowflake")
df = conn.query("SELECT * FROM my_table")
```

**Example 7: Caller's rights connection when running in Snowpark Container Services**

You can use "snowflake-callers-rights" type connections in any
environment running on Snowpark Container Services, including Streamlit in
Snowflake on containers and any self-managed caller's rights Service.

This will use the Snowpark-provided account, host, database, and schema to connect.
Additionally, it will set client\_session\_keep\_alive to True. These values
may be overridden with \*\*kwargs in st.connection. For a complete list
of keyword arguments, see the documentation for [snowflake.connector.connect()](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-api#label-snowflake-connector-methods-connect).

```
import streamlit as st

conn = st.connection("snowflake-callers-rights")
df = conn.query("SELECT * FROM my_table")
```

If you want to develop locally with a caller's rights connection, use an
environment variable to logically switch between a "snowflake"
connection locally and a "snowflake-callers-rights" connection in
Snowpark Container Services.

```
import streamlit as st

conn = (
    st.connection("snowflake")
    if "LOCAL_DEVELOPMENT" in st.secrets and st.secrets["LOCAL_DEVELOPMENT"]
    else st.connection("snowflake-callers-rights")
)
df = conn.query("SELECT * FROM my_table")
```

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/connections/snowflake_connection.py#L250 "View st.cursor source code on GitHub") | |
| --- | --- |
| SnowflakeConnection.cursor() | |
|  |  |
| --- | --- |
| Returns | |
| (snowflake.connector.cursor.SnowflakeCursor) | A cursor object for the connection. |

#### Example

The following example uses a cursor to insert multiple rows into a
table. The qmark parameter style is specified as an optional
keyword argument. Alternatively, the parameter style can be declared in
your connection configuration file. For more information, see the
[Snowflake Connector for Python documentation](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-example#using-qmark-or-numeric-binding).

```
import streamlit as st

conn = st.connection("snowflake", "paramstyle"="qmark")
rows_to_insert = [("Mary", "dog"), ("John", "cat"), ("Robert", "bird")]
conn.cursor().executemany(
    "INSERT INTO mytable (name, pet) VALUES (?, ?)", rows_to_insert
)
```

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/connections/snowflake_connection.py#L66 "View st.query source code on GitHub") | |
| --- | --- |
| SnowflakeConnection.query(sql, \*, ttl=None, show\_spinner="Running `snowflake.query(...)`.", params=None, \*\*kwargs) | |
| Parameters | |
| sql (str) | The read-only SQL query to execute. |
| ttl (float, int, timedelta or None) | The maximum number of seconds to keep results in the cache. If this is None (default), cached results do not expire with time. |
| show\_spinner (boolean or string) | Whether to enable the spinner. When a cached query is executed, no spinner is displayed because the result is immediately available. When a new query is executed, the default is to show a spinner with the message "Running snowflake.query(...)."  If this is False, no spinner displays while executing the query. If this is a string, the string will be used as the message for the spinner. |
| params (list, tuple, dict or None) | List of parameters to pass to the Snowflake Connector for Python Cursor.execute() method. This connector supports binding data to a SQL statement using qmark bindings. For more information and examples, see the [Snowflake Connector for Python documentation](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-example#using-qmark-or-numeric-binding). This defaults to None. |
|  |  |
| --- | --- |
| Returns | |
| (pandas.DataFrame) | The result of running the query, formatted as a pandas DataFrame. |

#### Example

```
import streamlit as st

conn = st.connection("snowflake")
df = conn.query("SELECT * FROM my_table")
st.dataframe(df)
```

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/connections/snowflake_connection.py#L283 "View st.raw_connection source code on GitHub") | |
| --- | --- |
| SnowflakeConnection.raw\_connection | |
|  |  |
| --- | --- |
| Returns | |
| (snowflake.connector.connection.SnowflakeConnection) | The connection object. |

#### Example

The following example uses a cursor to submit an asynchronous query,
saves the query ID, then periodically checks the query status through
the connection before retrieving the results.

```
import streamlit as st
import time

conn = st.connection("snowflake")
cur = conn.cursor()
cur.execute_async("SELECT * FROM my_table")
query_id = cur.sfqid
while True:
    status = conn.raw_connection.get_query_status(query_id)
    if conn.raw_connection.is_still_running(status):
        time.sleep(1)
    else:
        break
cur.get_results_from_sfqid(query_id)
df = cur.fetchall()
```

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/connections/base_connection.py#L134 "View st.reset source code on GitHub") | |
| --- | --- |
| SnowflakeConnection.reset() | |
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

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/connections/snowflake_connection.py#L322 "View st.session source code on GitHub") | |
| --- | --- |
| SnowflakeConnection.session() | |
|  |  |
| --- | --- |
| Returns | |
| (snowflake.snowpark.Session) | A new Snowpark session for this connection. |

#### Example

The following example creates a new Snowpark session and uses it to run
a query.

```
import streamlit as st

conn = st.connection("snowflake")
session = conn.session()
df = session.sql("SELECT * FROM my_table").collect()
```

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/connections/snowflake_connection.py#L168 "View st.write_pandas source code on GitHub") | |
| --- | --- |
| SnowflakeConnection.write\_pandas(df, table\_name, database=None, schema=None, chunk\_size=None, \*\*kwargs) | |
| Parameters | |
| df (pandas.DataFrame) | The pandas.DataFrame object containing the data to be copied into the table. |
| table\_name (str) | Name of the table where the data should be copied to. |
| database (str) | Name of the database containing the table. By default, the function writes to the database that is currently in use in the session.  Note  If you specify this parameter, you must also specify the schema parameter. |
| schema (str) | Name of the schema containing the table. By default, the function writes to the table in the schema that is currently in use in the session. |
| chunk\_size (int) | Number of elements to insert at a time. By default, the function inserts all elements in one chunk. |
| \*\*kwargs (Any) | Additional keyword arguments for snowflake.connector.pandas\_tools.write\_pandas(). |
|  |  |
| --- | --- |
| Returns | |
| (tuple[bool, int, int]) | A tuple containing three values:   1. A boolean value that is True if the write was successful. 2. An integer giving the number of chunks of data that were copied. 3. An integer giving the number of rows that were inserted. |

#### Example

The following example uses the database and schema currently in use in
the session and copies the data into a table named "my\_table."

```
import streamlit as st
import pandas as pd

df = pd.DataFrame(
    {"Name": ["Mary", "John", "Robert"], "Pet": ["dog", "cat", "bird"]}
)
conn = st.connection("snowflake")
conn.write_pandas(df, "my_table")
```

[*arrow\_back*Previous: st.connection](/develop/api-reference/connections/st.connection)[*arrow\_forward*Next: SQLConnection](/develop/api-reference/connections/st.connections.sqlconnection)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI