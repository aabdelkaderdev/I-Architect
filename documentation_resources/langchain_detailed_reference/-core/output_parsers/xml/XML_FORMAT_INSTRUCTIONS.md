<!-- Source: https://reference.langchain.com/python/langchain-core/output_parsers/xml/XML_FORMAT_INSTRUCTIONS -->

Attributev1.2.21 (latest)●Since v0.1

# XML\_FORMAT\_INSTRUCTIONS


```
XML_FORMAT_INSTRUCTIONS = 'The output should be formatted as a XML file.\n1. Output should conform to the tags below.\n2. If tags are not given, make them on your own.\n3. Remember to always open and close all the tags.\n\nAs an example, for the tags ["foo", "bar", "baz"]:\n1. String "<
  foo
>\n   <bar>\n      <baz></baz>\n   </bar>\n</foo>" is a well-formatted instance of the schema.\n2. String "<foo>\n   <bar>\n   </foo>" is a badly-formatted instance.\n3. String "<foo>\n   <tag>\n   </tag>\n</foo>" is a badly-formatted instance.\n\nHere are the output tags:\n```\n{tags}\n```'
```


