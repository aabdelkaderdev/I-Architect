<!-- Source: https://reference.langchain.com/python/langchain-core/utils/mustache -->

Modulev1.2.21 (latest)●Since v0.1

# mustache

Adapted from <https://github.com/noahmorrison/chevron>.

MIT License.

## Attributes

[attribute

logger](/python/langchain-core/utils/mustache/logger)[attribute

g\_token\_cache: dict[str, list[tuple[str, str]]]](/python/langchain-core/utils/mustache/g_token_cache)[attribute

EMPTY\_DICT: MappingProxyType[str, str]](/python/langchain-core/utils/mustache/EMPTY_DICT)

## Functions

[function

grab\_literal

Parse a literal from the template.](/python/langchain-core/utils/mustache/grab_literal)[function

l\_sa\_check

Do a preliminary check to see if a tag could be a standalone.](/python/langchain-core/utils/mustache/l_sa_check)[function

r\_sa\_check

Do a final check to see if a tag could be a standalone.](/python/langchain-core/utils/mustache/r_sa_check)[function

parse\_tag

Parse a tag from a template.](/python/langchain-core/utils/mustache/parse_tag)[function

tokenize

Tokenize a mustache template.

Tokenizes a mustache template in a generator fashion, using file-like objects. It
also accepts a string containing the template.](/python/langchain-core/utils/mustache/tokenize)[function

render

Render a mustache template.

Renders a mustache template with a data scope and inline partial capability.](/python/langchain-core/utils/mustache/render)

## Classes

[class

ChevronError

Custom exception for Chevron errors.](/python/langchain-core/utils/mustache/ChevronError)

## Type Aliases

[typeAlias

Scopes: TypeAlias](/python/langchain-core/utils/mustache/Scopes)


