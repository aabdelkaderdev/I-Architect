<!-- Source: https://reference.langchain.com/python/langchain-community/utilities/openapi/OpenAPISpec -->

Classv0.4.1 (latest)●Since v0.3

# OpenAPISpec

OpenAPI Model that removes mis-formatted parts of the spec.


```
OpenAPISpec()
```

## Bases

`OpenAPI`

## Attributes

[attribute

openapi: str](/python/langchain-community/utilities/openapi/OpenAPISpec/openapi)[attribute

base\_url: str

Get the base url.](/python/langchain-community/utilities/openapi/OpenAPISpec/base_url)

## Methods

[method

get\_referenced\_schema

Get a schema (or nested reference) or err.](/python/langchain-community/utilities/openapi/OpenAPISpec/get_referenced_schema)[method

get\_schema](/python/langchain-community/utilities/openapi/OpenAPISpec/get_schema)[method

parse\_obj](/python/langchain-community/utilities/openapi/OpenAPISpec/parse_obj)[method

from\_spec\_dict

Get an OpenAPI spec from a dict.](/python/langchain-community/utilities/openapi/OpenAPISpec/from_spec_dict)[method

from\_text

Get an OpenAPI spec from a text.](/python/langchain-community/utilities/openapi/OpenAPISpec/from_text)[method

from\_file

Get an OpenAPI spec from a file path.](/python/langchain-community/utilities/openapi/OpenAPISpec/from_file)[method

from\_url

Get an OpenAPI spec from a URL.](/python/langchain-community/utilities/openapi/OpenAPISpec/from_url)[method

get\_methods\_for\_path

Return a list of valid methods for the specified path.](/python/langchain-community/utilities/openapi/OpenAPISpec/get_methods_for_path)[method

get\_parameters\_for\_path](/python/langchain-community/utilities/openapi/OpenAPISpec/get_parameters_for_path)[method

get\_operation

Get the operation object for a given path and HTTP method.](/python/langchain-community/utilities/openapi/OpenAPISpec/get_operation)[method

get\_parameters\_for\_operation

Get the components for a given operation.](/python/langchain-community/utilities/openapi/OpenAPISpec/get_parameters_for_operation)[method

get\_request\_body\_for\_operation

Get the request body for a given operation.](/python/langchain-community/utilities/openapi/OpenAPISpec/get_request_body_for_operation)[method

get\_cleaned\_operation\_id

Get a cleaned operation id from an operation id.](/python/langchain-community/utilities/openapi/OpenAPISpec/get_cleaned_operation_id)


