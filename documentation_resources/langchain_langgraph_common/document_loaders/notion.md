<!-- Source: https://docs.langchain.com/oss/python/integrations/document_loaders/notion -->

> [Notion](https://www.notion.so/) is a collaboration platform with modified Markdown support that integrates kanban boards, tasks, wikis and databases. It is an all-in-one workspace for notetaking, knowledge and data management, and project and task management.

`NotionDBLoader` is a Python class for loading content from a `Notion` database. It retrieves pages from the database, reads their content, and returns a list of Document objects. `NotionDirectoryLoader` is used for loading data from a Notion database dump.

## [​](#requirements) Requirements

- A `Notion` Database
- Notion Integration Token

## [​](#setup) Setup

### [​](#1-create-a-notion-table-database) 1. Create a notion table Database

Create a new table database in Notion. You can add any column to the database and they will be treated as metadata. For example you can add the following columns:

- Title: set Title as the default property.
- Categories: A Multi-select property to store categories associated with the page.
- Keywords: A Multi-select property to store keywords associated with the page.

Add your content to the body of each page in the database. The NotionDBLoader will extract the content and metadata from these pages.

## [​](#2-create-a-notion-integration) 2. Create a notion integration

To create a Notion Integration, follow these steps:

1. Visit the [Notion Developers](https://www.notion.com/my-integrations) page and log in with your Notion account.
2. Click on the ”+ New integration” button.
3. Give your integration a name and choose the workspace where your database is located.
4. Select the require capabilities, this extension only need the Read content capability
5. Click the “Submit” button to create the integration.
   Once the integration is created, you’ll be provided with an `Integration Token (API key)`. Copy this token and keep it safe, as you’ll need it to use the NotionDBLoader.

### [​](#3-connect-the-integration-to-the-database) 3. Connect the integration to the Database

To connect your integration to the database, follow these steps:

1. Open your database in Notion.
2. Click on the three-dot menu icon in the top right corner of the database view.
3. Click on the ”+ New integration” button.
4. Find your integration, you may need to start typing its name in the search box.
5. Click on the “Connect” button to connect the integration to the database.

### [​](#4-get-the-database-id) 4. Get the Database ID

To get the database ID, follow these steps:

1. Open your database in Notion.
2. Click on the three-dot menu icon in the top right corner of the database view.
3. Select “Copy link” from the menu to copy the database URL to your clipboard.
4. The database ID is the long string of alphanumeric characters found in the URL. It typically looks like this: [www.notion.so/username/8935f9d140a04f95a872520c4f123456?v=](https://www.notion.so/username/8935f9d140a04f95a872520c4f123456?v=)… In this example, the database ID is 8935f9d140a04f95a872520c4f123456.

With the database properly set up and the integration token and database ID in hand, you can now use the NotionDBLoader code to load content and metadata from your Notion database.

### [​](#5-installation) 5. Installation

Instaall the `langchain-community` integration package.

Copy

```
pip install -qU langchain-community
```

## [​](#notion-database-loader) Notion Database loader

NotionDBLoader is part of the langchain package’s document loaders. You can use it as follows:

Copy

```
from getpass import getpass

NOTION_TOKEN = getpass()
DATABASE_ID = getpass()
```

Copy

```
········
········
```

Copy

```
from langchain_community.document_loaders import NotionDBLoader
```

Copy

```
loader = NotionDBLoader(
    integration_token=NOTION_TOKEN,
    database_id=DATABASE_ID,
    request_timeout_sec=30,  # optional, defaults to 10
)
```

Copy

```
docs = loader.load()
```

Copy

```
print(docs)
```

## [​](#notion-directory-loader) Notion directory loader

### [​](#setup-2) Setup

Export your dataset from Notion. You can do this by clicking on the three dots in the upper right hand corner and then clicking `Export`.
When exporting, make sure to select the `Markdown & CSV` format option.
This will produce a `.zip` file in your Downloads folder. Move the `.zip` file into this repository.
Run the following command to unzip the zip file (replace the `Export...` with your own file name as needed).

Copy

```
unzip Export-d3adfe0f-3131-4bf3-8987-a52017fc1bae.zip -d Notion_DB
```

### [​](#usage) Usage

Run the following command to ingest the data you just downloaded.

Copy

```
from langchain_community.document_loaders import NotionDirectoryLoader

loader = NotionDirectoryLoader("Notion_DB")
```

Copy

```
docs = loader.load()
```

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/document_loaders/notion.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.