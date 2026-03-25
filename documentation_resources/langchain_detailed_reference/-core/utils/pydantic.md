<!-- Source: https://reference.langchain.com/python/langchain-core/utils/pydantic -->

Modulev1.2.21 (latest)●Since v0.1

# pydantic

Utilities for pydantic.

## Attributes

[attribute

PYDANTIC\_VERSION](/python/langchain-core/utils/pydantic/PYDANTIC_VERSION)[attribute

PYDANTIC\_MAJOR\_VERSION](/python/langchain-core/utils/pydantic/PYDANTIC_MAJOR_VERSION)[attribute

PYDANTIC\_MINOR\_VERSION](/python/langchain-core/utils/pydantic/PYDANTIC_MINOR_VERSION)[attribute

IS\_PYDANTIC\_V1: bool](/python/langchain-core/utils/pydantic/IS_PYDANTIC_V1)[attribute

IS\_PYDANTIC\_V2: bool](/python/langchain-core/utils/pydantic/IS_PYDANTIC_V2)[attribute

PydanticBaseModel: BaseModel](/python/langchain-core/utils/pydantic/PydanticBaseModel)[attribute

TypeBaseModel: type[BaseModel]](/python/langchain-core/utils/pydantic/TypeBaseModel)[attribute

TBaseModel](/python/langchain-core/utils/pydantic/TBaseModel)[attribute

NO\_DEFAULT](/python/langchain-core/utils/pydantic/NO_DEFAULT)

## Functions

[function

is\_pydantic\_v1\_subclass

Check if the given class is Pydantic v1-like.](/python/langchain-core/utils/pydantic/is_pydantic_v1_subclass)[function

is\_pydantic\_v2\_subclass

Check if the given class is Pydantic v2-like.](/python/langchain-core/utils/pydantic/is_pydantic_v2_subclass)[function

is\_basemodel\_subclass

Check if the given class is a subclass of Pydantic `BaseModel`.

Check if the given class is a subclass of any of the following:

- `pydantic.BaseModel` in Pydantic 2.x
- `pydantic.v1.BaseModel` in Pydantic 2.x](/python/langchain-core/utils/pydantic/is_basemodel_subclass)[function

is\_basemodel\_instance

Check if the given class is an instance of Pydantic `BaseModel`.

Check if the given class is an instance of any of the following:

- `pydantic.BaseModel` in Pydantic 2.x
- `pydantic.v1.BaseModel` in Pydantic 2.x](/python/langchain-core/utils/pydantic/is_basemodel_instance)[function

pre\_init

Decorator to run a function before model initialization.](/python/langchain-core/utils/pydantic/pre_init)[function

get\_fields

Return the field names of a Pydantic model.](/python/langchain-core/utils/pydantic/get_fields)[function

create\_model

Create a Pydantic model with the given field definitions.

Please use `create_model_v2` instead of this function.](/python/langchain-core/utils/pydantic/create_model)[function

create\_model\_v2

Create a Pydantic model with the given field definitions.

Warning

Do not use outside of langchain packages. This API is subject to change at any
time.](/python/langchain-core/utils/pydantic/create_model_v2)[deprecatedfunction

get\_pydantic\_major\_version

DEPRECATED - Get the major version of Pydantic.

Use `PYDANTIC_VERSION.major` instead.](/python/langchain-core/utils/pydantic/get_pydantic_major_version)


