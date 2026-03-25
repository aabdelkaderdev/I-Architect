<!-- Source: https://reference.langchain.com/python/langchain-community/utilities/pebblo -->

Modulev0.4.1 (latest)●Since v0.3

# pebblo

## Attributes

[attribute

logger](/python/langchain-community/utilities/pebblo/logger)[attribute

PLUGIN\_VERSION: str](/python/langchain-community/utilities/pebblo/PLUGIN_VERSION)[attribute

BATCH\_SIZE\_BYTES: int](/python/langchain-community/utilities/pebblo/BATCH_SIZE_BYTES)[attribute

file\_loader: list](/python/langchain-community/utilities/pebblo/file_loader)[attribute

dir\_loader: list](/python/langchain-community/utilities/pebblo/dir_loader)[attribute

in\_memory: list](/python/langchain-community/utilities/pebblo/in_memory)[attribute

cloud\_folder: list](/python/langchain-community/utilities/pebblo/cloud_folder)[attribute

LOADER\_TYPE\_MAPPING: dict](/python/langchain-community/utilities/pebblo/LOADER_TYPE_MAPPING)

## Functions

[function

get\_full\_path

Return an absolute local path for a local file/directory,
for a network related path, return as is.](/python/langchain-community/utilities/pebblo/get_full_path)[function

get\_loader\_type

Return loader type among, file, dir or in-memory.](/python/langchain-community/utilities/pebblo/get_loader_type)[function

get\_loader\_full\_path

Return an absolute source path of source of loader based on the
keys present in Document.](/python/langchain-community/utilities/pebblo/get_loader_full_path)[function

get\_runtime

Fetch the current Framework and Runtime details.](/python/langchain-community/utilities/pebblo/get_runtime)[function

get\_ip

Fetch local runtime ip address.](/python/langchain-community/utilities/pebblo/get_ip)[function

generate\_size\_based\_batches

Generate batches of documents based on page\_content size.
Args:
docs: List of documents to be batched.
max\_batch\_size: Maximum size of each batch in bytes. Defaults to 100\*1024(100KB)
Returns:
List[List[Document]]: List of batches of documents](/python/langchain-community/utilities/pebblo/generate_size_based_batches)[function

get\_file\_owner\_from\_path

Fetch owner of local file path.](/python/langchain-community/utilities/pebblo/get_file_owner_from_path)[function

get\_source\_size

Fetch size of source path. Source can be a directory or a file.](/python/langchain-community/utilities/pebblo/get_source_size)[function

calculate\_content\_size

Calculate the content size in bytes:

- Encode the string to bytes using a specific encoding (e.g., UTF-8)
- Get the length of the encoded bytes.](/python/langchain-community/utilities/pebblo/calculate_content_size)

## Classes

[class

Routes

Routes available for the Pebblo API as enumerator.](/python/langchain-community/utilities/pebblo/Routes)[class

IndexedDocument

Pebblo Indexed Document.](/python/langchain-community/utilities/pebblo/IndexedDocument)[class

Runtime

Pebblo Runtime.](/python/langchain-community/utilities/pebblo/Runtime)[class

Framework

Pebblo Framework instance.](/python/langchain-community/utilities/pebblo/Framework)[class

App

Pebblo AI application.](/python/langchain-community/utilities/pebblo/App)[class

Doc

Pebblo document.](/python/langchain-community/utilities/pebblo/Doc)[class

PebbloLoaderAPIWrapper

Wrapper for Pebblo Loader API.](/python/langchain-community/utilities/pebblo/PebbloLoaderAPIWrapper)


