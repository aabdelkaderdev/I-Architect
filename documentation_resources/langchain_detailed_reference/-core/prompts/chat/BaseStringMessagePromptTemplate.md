<!-- Source: https://reference.langchain.com/python/langchain-core/prompts/chat/BaseStringMessagePromptTemplate -->

Classv1.2.21 (latest)●Since v0.1

# BaseStringMessagePromptTemplate

Base class for message prompt templates that use a string prompt template.


```
BaseStringMessagePromptTemplate(
  self,
  *args: Any = (),
  **kwargs: Any = {}
)
```

## Bases

`BaseMessagePromptTemplate``ABC`

## Attributes

[attribute

prompt: StringPromptTemplate

String prompt template.](/python/langchain-core/prompts/chat/BaseStringMessagePromptTemplate/prompt)[attribute

additional\_kwargs: dict

Additional keyword arguments to pass to the prompt template.](/python/langchain-core/prompts/chat/BaseStringMessagePromptTemplate/additional_kwargs)[attribute

input\_variables: list[str]

Input variables for this prompt template.](/python/langchain-core/prompts/chat/BaseStringMessagePromptTemplate/input_variables)

## Methods

[method

from\_template

Create a class from a string template.](/python/langchain-core/prompts/chat/BaseStringMessagePromptTemplate/from_template)[method

from\_template\_file

Create a class from a template file.](/python/langchain-core/prompts/chat/BaseStringMessagePromptTemplate/from_template_file)[method

format

Format the prompt template.](/python/langchain-core/prompts/chat/BaseStringMessagePromptTemplate/format)[method

aformat

Async format the prompt template.](/python/langchain-core/prompts/chat/BaseStringMessagePromptTemplate/aformat)[method

format\_messages

Format messages from kwargs.](/python/langchain-core/prompts/chat/BaseStringMessagePromptTemplate/format_messages)[method

aformat\_messages

Async format messages from kwargs.](/python/langchain-core/prompts/chat/BaseStringMessagePromptTemplate/aformat_messages)[method

pretty\_repr

Human-readable representation.](/python/langchain-core/prompts/chat/BaseStringMessagePromptTemplate/pretty_repr)

## Inherited from[BaseMessagePromptTemplate](/python/langchain-core/prompts/message/BaseMessagePromptTemplate)

### Methods

[Mis\_lc\_serializable

—

Return `True` as this class is serializable.](/python/langchain-core/prompts/message/BaseMessagePromptTemplate/is_lc_serializable)[Mget\_lc\_namespace

—

Get the namespace of the LangChain object.](/python/langchain-core/prompts/message/BaseMessagePromptTemplate/get_lc_namespace)[Mpretty\_print

—

Print a human-readable representation.](/python/langchain-core/prompts/message/BaseMessagePromptTemplate/pretty_print)

## Inherited from[Serializable](/python/langchain-core/load/serializable/Serializable)

### Attributes

[Alc\_secrets: dict[str, str]

—

A map of constructor argument names to secret ids.](/python/langchain-core/load/serializable/Serializable/lc_secrets)[Alc\_attributes: dict

—

List of attribute names that should be included in the serialized kwargs.](/python/langchain-core/load/serializable/Serializable/lc_attributes)[Amodel\_config](/python/langchain-core/load/serializable/Serializable/model_config)

### Methods

[Mis\_lc\_serializable

—

Is this class serializable?](/python/langchain-core/load/serializable/Serializable/is_lc_serializable)[Mget\_lc\_namespace

—

Get the namespace of the LangChain object.](/python/langchain-core/load/serializable/Serializable/get_lc_namespace)[Mlc\_id

—

Return a unique identifier for this class for serialization purposes.](/python/langchain-core/load/serializable/Serializable/lc_id)[Mto\_json

—

Serialize the object to JSON.](/python/langchain-core/load/serializable/Serializable/to_json)[Mto\_json\_not\_implemented

—

Serialize a "not implemented" object.](/python/langchain-core/load/serializable/Serializable/to_json_not_implemented)


