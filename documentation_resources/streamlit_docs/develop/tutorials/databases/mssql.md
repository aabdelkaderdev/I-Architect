<!-- Source: https://docs.streamlit.io/develop/tutorials/databases/mssql -->

This guide explains how to securely access a ***remote*** Microsoft SQL Server database from Streamlit Community Cloud. It uses the [pyodbc](https://github.com/mkleehammer/pyodbc/wiki) library and Streamlit's [Secrets management](/develop/concepts/connections/secrets-management).

If you already have a remote database that you want to use, feel free
to [skip to the next step](/develop/tutorials/databases/mssql#add-username-and-password-to-your-local-app-secrets).

First, follow the Microsoft documentation to install [SQL Server](https://docs.microsoft.com/en-gb/sql/sql-server/?view=sql-server-ver15) and the `sqlcmd` [Utility](https://docs.microsoft.com/en-gb/sql/tools/sqlcmd-utility?view=sql-server-ver15). They have detailed installation guides on how to:

- [Install SQL Server on Windows](https://docs.microsoft.com/en-gb/sql/database-engine/install-windows/install-sql-server?view=sql-server-ver15)
- [Install on Red Hat Enterprise Linux](https://docs.microsoft.com/en-gb/sql/linux/quickstart-install-connect-red-hat?view=sql-server-ver15)
- [Install on SUSE Linux Enterprise Server](https://docs.microsoft.com/en-gb/sql/linux/quickstart-install-connect-suse?view=sql-server-ver15)
- [Install on Ubuntu](https://docs.microsoft.com/en-gb/sql/linux/quickstart-install-connect-ubuntu?view=sql-server-ver15)
- [Run on Docker](https://docs.microsoft.com/en-gb/sql/linux/quickstart-install-connect-docker?view=sql-server-ver15)
- [Provision a SQL VM in Azure](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/sql/provision-sql-server-linux-virtual-machine?toc=/sql/toc/toc.json)

Once you have SQL Server installed, note down your SQL Server name, username, and password during setup.

If you are connecting locally, use `sqlcmd` to connect to your new local SQL Server instance.

1. In your terminal, run the following command:

   ```
   sqlcmd -S localhost -U SA -P '<YourPassword>'
   ```

   As you are connecting locally, the SQL Server name is `localhost`, the username is `SA`, and the password is the one you provided during the SA account setup.
2. You should see a **sqlcmd** command prompt `1>`, if successful.
3. If you run into a connection failure, review Microsoft's connection troubleshooting recommendations for your OS ([Linux](https://docs.microsoft.com/en-gb/sql/linux/sql-server-linux-troubleshooting-guide?view=sql-server-ver15#connection) & [Windows](https://docs.microsoft.com/en-gb/sql/linux/sql-server-linux-troubleshooting-guide?view=sql-server-ver15#connection)).

When connecting remotely, the SQL Server name is the machine name or IP address. You might also need to open the SQL Server TCP port (default 1433) on your firewall.

By now, you have SQL Server running and have connected to it with `sqlcmd`! 🥳 Let's put it to use by creating a database containing a table with some example values.

1. From the `sqlcmd` command prompt, run the following Transact-SQL command to create a test database `mydb`:

   ```
   CREATE DATABASE mydb
   ```
2. To execute the above command, type `GO` on a new line:

   ```
   GO
   ```

Next create a new table, `mytable`, in the `mydb` database with three columns and two rows.

1. Switch to the new `mydb` database:

   ```
   USE mydb
   ```
2. Create a new table with the following schema:

   ```
   CREATE TABLE mytable (name varchar(80), pet varchar(80))
   ```
3. Insert some data into the table:

   ```
   INSERT INTO mytable VALUES ('Mary', 'dog'), ('John', 'cat'), ('Robert', 'bird')
   ```
4. Type `GO` to execute the above commands:

   ```
   GO
   ```

To end your **sqlcmd** session, type `QUIT` on a new line.

Your local Streamlit app will read secrets from a file `.streamlit/secrets.toml` in your app's root directory. Create this file if it doesn't exist yet and add the SQL Server name, database name, username, and password as shown below:

```
# .streamlit/secrets.toml

server = "localhost"
database = "mydb"
username = "SA"
password = "xxx"
```

When copying your app secrets to Streamlit Community Cloud, be sure to replace the values of **server**, **database**, **username**, and **password** with those of your *remote* SQL Server!

And add this file to `.gitignore` and don't commit it to your GitHub repo.

As the `secrets.toml` file above is not committed to GitHub, you need to pass its content to your deployed app (on Streamlit Community Cloud) separately. Go to the [app dashboard](https://share.streamlit.io/) and in the app's dropdown menu, click on **Edit Secrets**. Copy the content of `secrets.toml` into the text area. More information is available at [Secrets management](/deploy/streamlit-community-cloud/deploy-your-app/secrets-management).

To connect to SQL Server *locally* with Streamlit, you need to `pip install pyodbc`, in addition to the Microsoft ODBC driver you installed during the SQL Server installation.

On *Streamlit Cloud*, we have built-in support for SQL Server. On popular demand, we directly added SQL Server tools including the ODBC drivers and the executables `sqlcmd` and `bcp` to the container image for Cloud apps, so you don't need to install them.

All you need to do is add the [`pyodbc`](https://github.com/mkleehammer/pyodbc) Python package to your `requirements.txt` file, and you're ready to go! 🎈

```
# requirements.txt
pyodbc==x.x.x
```

Replace `x.x.x` ☝️ with the version of pyodbc you want installed on Cloud.

At this time, Streamlit Community Cloud does not support Azure Active Directory authentication. We will update this tutorial when we add support for Azure Active Directory.

Copy the code below to your Streamlit app and run it. Make sure to adapt `query` to use the name of your table.

```
import streamlit as st
import pyodbc

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + st.secrets["server"]
        + ";DATABASE="
        + st.secrets["database"]
        + ";UID="
        + st.secrets["username"]
        + ";PWD="
        + st.secrets["password"]
    )

conn = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from mytable;")

# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")
```

See `st.cache_data` above? Without it, Streamlit would run the query every time the app reruns (e.g. on a widget interaction). With `st.cache_data`, it only runs when the query changes or after 10 minutes (that's what `ttl` is for). Watch out: If your database updates more frequently, you should adapt `ttl` or remove caching so viewers always see the latest data. Learn more in [Caching](/develop/concepts/architecture/caching).

If everything worked out (and you used the example table we created above), your app should look like this:

[*arrow\_back*Previous: Google Cloud Storage](/develop/tutorials/databases/gcs)[*arrow\_forward*Next: MongoDB](/develop/tutorials/databases/mongodb)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI