<!-- Source: https://docs.streamlit.io/develop/tutorials/databases/private-gsheet -->

This guide explains how to securely access a private Google Sheet from Streamlit Community Cloud. It uses [st.connection](/develop/api-reference/connections/st.connection), [Streamlit GSheetsConnection](https://github.com/streamlit/gsheets-connection), and Streamlit's [Secrets management](/develop/concepts/connections/secrets-management).

If you are fine with enabling link sharing for your Google Sheet (i.e. everyone with the link can view it), the guide [Connect Streamlit to a public Google Sheet](/develop/tutorials/databases/public-gsheet) shows a simpler method of doing this. If your Sheet contains sensitive information and you cannot enable link sharing, keep on reading.

This tutorial requires `streamlit>=1.28` and `st-gsheets-connection` in your Python environment.

If you already have a Sheet that you want to use, you can [skip to the next step](/develop/tutorials/databases/private-gsheet#enable-the-sheets-api).

Create a spreadsheet with this example data.

| name | pet |
| --- | --- |
| Mary | dog |
| John | cat |
| Robert | bird |

Programmatic access to Google Sheets is controlled through [Google Cloud Platform](https://cloud.google.com/). Create an account or sign in and head over to the [**APIs & Services** dashboard](https://console.cloud.google.com/apis/dashboard) (select or create a project if asked). As shown below, search for the Sheets API and enable it:

To use the Sheets API from Streamlit Community Cloud, you need a Google Cloud Platform service account (a special account type for programmatic data access). Go to the [**Service Accounts** page](https://console.cloud.google.com/iam-admin/serviceaccounts) and create an account with the **Viewer** permission (this will let the account access data but not change it):

The button "**CREATE SERVICE ACCOUNT**" is gray, you don't have the correct permissions. Ask the admin of your Google Cloud project for help.

After clicking "**DONE**", you should be back on the service accounts overview. First, note down the email address of the account you just created (**important for next step!**). Then, create a JSON key file for the new account and download it:

By default, the service account you just created cannot access your Google Sheet. To give it access, click on the "**Share**" button in the Google Sheet, add the email of the service account (noted down in step 2), and choose the correct permission (if you just want to read the data, "**Viewer**" is enough):

Your local Streamlit app will read secrets from a file `.streamlit/secrets.toml` in your app's root directory. Create this file if it doesn't exist yet and add the URL of your Google Sheet plus the content of the key file you downloaded to it as shown below:

```
# .streamlit/secrets.toml

[connections.gsheets]
spreadsheet = "https://docs.google.com/spreadsheets/d/xxxxxxx/edit#gid=0"

# From your JSON key file
type = "service_account"
project_id = "xxx"
private_key_id = "xxx"
private_key = "xxx"
client_email = "xxx"
client_id = "xxx"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "xxx"
```

Add this file to `.gitignore` and don't commit it to your GitHub repo!

Copy the code below to your Streamlit app and run it.

```
# streamlit_app.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read()

# Print results.
for row in df.itertuples():
    st.write(f"{row.name} has a :{row.pet}:")
```

See `st.connection` above? This handles secrets retrieval, setup, query caching and retries. By default, `.read()` results are cached without expiring. You can pass optional parameters to `.read()` to customize your connection. For example, you can specify the name of a worksheet, cache expiration time, or pass-through parameters for [`pandas.read_csv`](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html) like this:

```
df = conn.read(
    worksheet="Sheet1",
    ttl="10m",
    usecols=[0, 1],
    nrows=3,
)
```

In this case, we set `ttl="10m"` to ensure the query result is cached for no longer than 10 minutes. You can also set `ttl=0` to disable caching. Learn more in [Caching](/develop/concepts/architecture/caching). We've declared optional parameters `usecols=[0,1]` and `nrows=3` for `pandas` to use under the hood.

If everything worked out (and you used the example table we created above), your app should look like this:

This tutorial assumes a local Streamlit app, however you can also connect to Google Sheets from apps hosted in Community Cloud. The main additional steps are:

- [Include information about dependencies](/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies) using a `requirements.txt` file with `st-gsheets-connection` and any other dependencies.
- [Add your secrets](/deploy/streamlit-community-cloud/deploy-your-app/secrets-management) to your Community Cloud app.

[*arrow\_back*Previous: PostgreSQL](/develop/tutorials/databases/postgresql)[*arrow\_forward*Next: Public Google Sheet](/develop/tutorials/databases/public-gsheet)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI