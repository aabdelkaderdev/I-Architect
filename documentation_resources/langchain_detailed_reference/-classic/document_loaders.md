<!-- Source: https://reference.langchain.com/python/langchain-classic/document_loaders -->

Modulev1.2.13 (latest)●Since v1.0

# document\_loaders

**Document Loaders** are classes to load Documents.

**Document Loaders** are usually used to load a lot of Documents in a single run.

## Attributes

[attribute

DEPRECATED\_LOOKUP: dict](/python/langchain-classic/document_loaders/DEPRECATED_LOOKUP)

## Functions

[function

create\_importer

Create a function that helps retrieve objects from their new locations.

The goal of this function is to help users transition from deprecated
imports to new imports.

The function will raise deprecation warning on loops using
`deprecated_lookups` or `fallback_module`.

Module lookups will import without deprecation warnings (used to speed
up imports from large namespaces like llms or chat models).

This function should ideally only be used with deprecated imports not with
existing imports that are valid, as in addition to raising deprecation warnings
the dynamic imports can create other issues for developers (e.g.,
loss of type information, IDE support for going to definition etc).](/python/langchain-classic/_api/module_import/create_importer)

## Modules

[module

evernote](/python/langchain-classic/document_loaders/evernote)[module

merge](/python/langchain-classic/document_loaders/merge)[module

open\_city\_data](/python/langchain-classic/document_loaders/open_city_data)[module

notion](/python/langchain-classic/document_loaders/notion)[module

azure\_blob\_storage\_file](/python/langchain-classic/document_loaders/azure_blob_storage_file)[module

lakefs](/python/langchain-classic/document_loaders/lakefs)[module

sharepoint](/python/langchain-classic/document_loaders/sharepoint)[module

quip](/python/langchain-classic/document_loaders/quip)[module

airbyte\_json](/python/langchain-classic/document_loaders/airbyte_json)[module

facebook\_chat](/python/langchain-classic/document_loaders/facebook_chat)[module

recursive\_url\_loader](/python/langchain-classic/document_loaders/recursive_url_loader)[module

stripe](/python/langchain-classic/document_loaders/stripe)[module

hn](/python/langchain-classic/document_loaders/hn)[module

base\_o365](/python/langchain-classic/document_loaders/base_o365)[module

tensorflow\_datasets](/python/langchain-classic/document_loaders/tensorflow_datasets)[module

airbyte](/python/langchain-classic/document_loaders/airbyte)[module

rspace](/python/langchain-classic/document_loaders/rspace)[module

arxiv](/python/langchain-classic/document_loaders/arxiv)[module

rocksetdb](/python/langchain-classic/document_loaders/rocksetdb)[module

news](/python/langchain-classic/document_loaders/news)[module

google\_speech\_to\_text](/python/langchain-classic/document_loaders/google_speech_to_text)[module

onedrive\_file](/python/langchain-classic/document_loaders/onedrive_file)[module

docusaurus](/python/langchain-classic/document_loaders/docusaurus)[module

mhtml](/python/langchain-classic/document_loaders/mhtml)[module

psychic](/python/langchain-classic/document_loaders/psychic)[module

odt](/python/langchain-classic/document_loaders/odt)[module

roam](/python/langchain-classic/document_loaders/roam)[module

powerpoint](/python/langchain-classic/document_loaders/powerpoint)[module

async\_html](/python/langchain-classic/document_loaders/async_html)[module

base](/python/langchain-classic/document_loaders/base)[module

url\_playwright](/python/langchain-classic/document_loaders/url_playwright)[module

couchbase](/python/langchain-classic/document_loaders/couchbase)[module

cube\_semantic](/python/langchain-classic/document_loaders/cube_semantic)[module

baiducloud\_bos\_file](/python/langchain-classic/document_loaders/baiducloud_bos_file)[module

notiondb](/python/langchain-classic/document_loaders/notiondb)[module

unstructured](/python/langchain-classic/document_loaders/unstructured)[module

markdown](/python/langchain-classic/document_loaders/markdown)[module

rst](/python/langchain-classic/document_loaders/rst)[module

browserless](/python/langchain-classic/document_loaders/browserless)[module

figma](/python/langchain-classic/document_loaders/figma)[module

imsdb](/python/langchain-classic/document_loaders/imsdb)[module

whatsapp\_chat](/python/langchain-classic/document_loaders/whatsapp_chat)[module

reddit](/python/langchain-classic/document_loaders/reddit)[module

pdf](/python/langchain-classic/document_loaders/pdf)[module

pyspark\_dataframe](/python/langchain-classic/document_loaders/pyspark_dataframe)[module

onedrive](/python/langchain-classic/document_loaders/onedrive)[module

url\_selenium](/python/langchain-classic/document_loaders/url_selenium)[module

hugging\_face\_dataset](/python/langchain-classic/document_loaders/hugging_face_dataset)[module

telegram](/python/langchain-classic/document_loaders/telegram)[module

chromium](/python/langchain-classic/document_loaders/chromium)[module

baiducloud\_bos\_directory](/python/langchain-classic/document_loaders/baiducloud_bos_directory)[module

assemblyai](/python/langchain-classic/document_loaders/assemblyai)[module

readthedocs](/python/langchain-classic/document_loaders/readthedocs)[module

git](/python/langchain-classic/document_loaders/git)[module

html](/python/langchain-classic/document_loaders/html)[module

dataframe](/python/langchain-classic/document_loaders/dataframe)[module

rtf](/python/langchain-classic/document_loaders/rtf)[module

dropbox](/python/langchain-classic/document_loaders/dropbox)[module

python](/python/langchain-classic/document_loaders/python)[module

helpers](/python/langchain-classic/document_loaders/helpers)[module

tencent\_cos\_file](/python/langchain-classic/document_loaders/tencent_cos_file)[module

web\_base](/python/langchain-classic/document_loaders/web_base)[module

mongodb](/python/langchain-classic/document_loaders/mongodb)[module

ifixit](/python/langchain-classic/document_loaders/ifixit)[module

twitter](/python/langchain-classic/document_loaders/twitter)[module

apify\_dataset](/python/langchain-classic/document_loaders/apify_dataset)[module

image\_captions](/python/langchain-classic/document_loaders/image_captions)[module

s3\_directory](/python/langchain-classic/document_loaders/s3_directory)[module

tencent\_cos\_directory](/python/langchain-classic/document_loaders/tencent_cos_directory)[module

directory](/python/langchain-classic/document_loaders/directory)[module

email](/python/langchain-classic/document_loaders/email)[module

nuclia](/python/langchain-classic/document_loaders/nuclia)[module

github](/python/langchain-classic/document_loaders/github)[module

s3\_file](/python/langchain-classic/document_loaders/s3_file)[module

youtube](/python/langchain-classic/document_loaders/youtube)[module

spreedly](/python/langchain-classic/document_loaders/spreedly)[module

trello](/python/langchain-classic/document_loaders/trello)[module

etherscan](/python/langchain-classic/document_loaders/etherscan)[module

geodataframe](/python/langchain-classic/document_loaders/geodataframe)[module

obs\_directory](/python/langchain-classic/document_loaders/obs_directory)[module

pubmed](/python/langchain-classic/document_loaders/pubmed)[module

url](/python/langchain-classic/document_loaders/url)[module

gitbook](/python/langchain-classic/document_loaders/gitbook)[module

mastodon](/python/langchain-classic/document_loaders/mastodon)[module

tsv](/python/langchain-classic/document_loaders/tsv)[module

modern\_treasury](/python/langchain-classic/document_loaders/modern_treasury)[module

srt](/python/langchain-classic/document_loaders/srt)[module

notebook](/python/langchain-classic/document_loaders/notebook)[module

polars\_dataframe](/python/langchain-classic/document_loaders/polars_dataframe)[module

sitemap](/python/langchain-classic/document_loaders/sitemap)[module

slack\_directory](/python/langchain-classic/document_loaders/slack_directory)[module

json\_loader](/python/langchain-classic/document_loaders/json_loader)[module

generic](/python/langchain-classic/document_loaders/generic)[module

blockchain](/python/langchain-classic/document_loaders/blockchain)[module

bigquery](/python/langchain-classic/document_loaders/bigquery)[module

tomarkdown](/python/langchain-classic/document_loaders/tomarkdown)[module

brave\_search](/python/langchain-classic/document_loaders/brave_search)[module

googledrive](/python/langchain-classic/document_loaders/googledrive)[module

org\_mode](/python/langchain-classic/document_loaders/org_mode)[module

college\_confidential](/python/langchain-classic/document_loaders/college_confidential)[module

max\_compute](/python/langchain-classic/document_loaders/max_compute)[module

datadog\_logs](/python/langchain-classic/document_loaders/datadog_logs)[module

conllu](/python/langchain-classic/document_loaders/conllu)[module

csv\_loader](/python/langchain-classic/document_loaders/csv_loader)[module

acreom](/python/langchain-classic/document_loaders/acreom)[module

toml](/python/langchain-classic/document_loaders/toml)[module

concurrent](/python/langchain-classic/document_loaders/concurrent)[module

fauna](/python/langchain-classic/document_loaders/fauna)[module

xorbits](/python/langchain-classic/document_loaders/xorbits)[module

gutenberg](/python/langchain-classic/document_loaders/gutenberg)[module

docugami](/python/langchain-classic/document_loaders/docugami)[module

arcgis\_loader](/python/langchain-classic/document_loaders/arcgis_loader)[module

discord](/python/langchain-classic/document_loaders/discord)[module

onenote](/python/langchain-classic/document_loaders/onenote)[module

word\_document](/python/langchain-classic/document_loaders/word_document)[module

text](/python/langchain-classic/document_loaders/text)[module

snowflake\_loader](/python/langchain-classic/document_loaders/snowflake_loader)[module

image](/python/langchain-classic/document_loaders/image)[module

azlyrics](/python/langchain-classic/document_loaders/azlyrics)[module

duckdb\_loader](/python/langchain-classic/document_loaders/duckdb_loader)[module

weather](/python/langchain-classic/document_loaders/weather)[module

airtable](/python/langchain-classic/document_loaders/airtable)[module

blackboard](/python/langchain-classic/document_loaders/blackboard)[module

azure\_blob\_storage\_container](/python/langchain-classic/document_loaders/azure_blob_storage_container)[module

obs\_file](/python/langchain-classic/document_loaders/obs_file)[module

joplin](/python/langchain-classic/document_loaders/joplin)[module

bibtex](/python/langchain-classic/document_loaders/bibtex)[module

iugu](/python/langchain-classic/document_loaders/iugu)[module

rss](/python/langchain-classic/document_loaders/rss)[module

wikipedia](/python/langchain-classic/document_loaders/wikipedia)[module

chatgpt](/python/langchain-classic/document_loaders/chatgpt)[module

confluence](/python/langchain-classic/document_loaders/confluence)[module

gcs\_directory](/python/langchain-classic/document_loaders/gcs_directory)[module

epub](/python/langchain-classic/document_loaders/epub)[module

html\_bs](/python/langchain-classic/document_loaders/html_bs)[module

diffbot](/python/langchain-classic/document_loaders/diffbot)[module

mediawikidump](/python/langchain-classic/document_loaders/mediawikidump)[module

xml](/python/langchain-classic/document_loaders/xml)[module

bilibili](/python/langchain-classic/document_loaders/bilibili)[module

azure\_ai\_data](/python/langchain-classic/document_loaders/azure_ai_data)[module

gcs\_file](/python/langchain-classic/document_loaders/gcs_file)[module

excel](/python/langchain-classic/document_loaders/excel)[module

larksuite](/python/langchain-classic/document_loaders/larksuite)[module

obsidian](/python/langchain-classic/document_loaders/obsidian)[module

blob\_loaders](/python/langchain-classic/document_loaders/blob_loaders)[module

parsers](/python/langchain-classic/document_loaders/parsers)


