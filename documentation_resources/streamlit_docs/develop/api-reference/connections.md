<!-- Source: https://docs.streamlit.io/develop/api-reference/connections -->

[#### Create a connection

Connect to a data source or API

```
conn = st.connection('pets_db', type='sql')
pet_owners = conn.query('select * from pet_owners')
st.dataframe(pet_owners)
```](/develop/api-reference/connections/st.connection)

[#### SnowflakeConnection

A connection to Snowflake.

```
conn = st.connection('snowflake')
```](/develop/api-reference/connections/st.connections.snowflakeconnection)[#### SQLConnection

A connection to a SQL database using SQLAlchemy.

```
conn = st.connection('sql')
```](/develop/api-reference/connections/st.connections.sqlconnection)

[#### Connection base class

Build your own connection with `BaseConnection`.

```
class MyConnection(BaseConnection[myconn.MyConnection]):
    def _connect(self, **kwargs) -> MyConnection:
        return myconn.connect(**self._secrets, **kwargs)
    def query(self, query):
        return self._instance.query(query)
```](/develop/api-reference/connections/st.connections.baseconnection)

[#### Secrets singleton

Access secrets from a local TOML file.

```
key = st.secrets["OpenAI_key"]
```](/develop/api-reference/connections/st.secrets)[#### Secrets file

Save your secrets in a per-project or per-profile TOML file.

```
OpenAI_key = "<YOUR_SECRET_KEY>"
```](/develop/api-reference/connections/secrets.toml)

[*delete*

#### SnowparkConnection

A connection to Snowflake.

```
conn = st.connection("snowpark")
```](/develop/api-reference/connections/st.connections.snowparkconnection)

[*arrow\_back*Previous: Caching and state](/develop/api-reference/caching-and-state)[*arrow\_forward*Next: st.secrets](/develop/api-reference/connections/st.secrets)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI