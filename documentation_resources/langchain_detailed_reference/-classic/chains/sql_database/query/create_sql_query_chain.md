<!-- Source: https://reference.langchain.com/python/langchain-classic/chains/sql_database/query/create_sql_query_chain -->

Functionv1.2.13 (latest)●Since v1.0

# create\_sql\_query\_chain

Create a chain that generates SQL queries.

*Security Note*: This chain generates SQL queries for the given database.

```
The SQLDatabase class provides a get_table_info method that can be used
to get column information as well as sample data from the table.

To mitigate risk of leaking sensitive data, limit permissions
to read and scope to the tables that are needed.

Optionally, use the SQLInputWithTables input type to specify which tables
are allowed to be accessed.

Control access to who can submit requests to this chain.

See https://docs.langchain.com/oss/python/security-policy for more information.
```


```
create_sql_query_chain(
  llm: BaseLanguageModel,
  db: SQLDatabase,
  prompt: BasePromptTemplate | None = None,
  k: int = 5,
  *,
  get_col_comments: bool | None = None
) -> Runnable[SQLInput | SQLInputWithTables | dict[str, Any], str]
```

**Example:**

```
# pip install -U langchain langchain-community langchain-openai
from langchain_openai import ChatOpenAI
from langchain_classic.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///Chinook.db")
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
chain = create_sql_query_chain(model, db)
response = chain.invoke({"question": "How many employees are there"})
```

**Prompt:**

If no prompt is provided, a default prompt is selected based on the SQLDatabase
dialect. If one is provided, it must support input variables:

```
* input: The user question plus suffix "\\nSQLQuery: " is passed here.
* top_k: The number of results per select statement (the `k` argument to
    this function) is passed in here.
* table_info: Table definitions and sample rows are passed in here. If the
    user specifies "table_names_to_use" when invoking chain, only those
    will be included. Otherwise, all tables are included.
* dialect (optional): If dialect input variable is in prompt, the db
    dialect will be passed in here.
```

Here's an example prompt:

```
from langchain_core.prompts import PromptTemplate

template = '''Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Only use the following tables:

{table_info}.

Question: {input}'''
prompt = PromptTemplate.from_template(template)
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `llm`\* | `BaseLanguageModel` | The language model to use. |
| `db`\* | `SQLDatabase` | The SQLDatabase to generate the query for. |
| `prompt` | `BasePromptTemplate | None` | Default:`None`  The prompt to use. If none is provided, will choose one based on dialect. See Prompt section below for more. |
| `k` | `int` | Default:`5`  The number of results per select statement to return. |
| `get_col_comments` | `bool | None` | Default:`None`  Whether to retrieve column comments along with table info. |


