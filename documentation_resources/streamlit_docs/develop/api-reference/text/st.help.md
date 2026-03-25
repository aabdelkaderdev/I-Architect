<!-- Source: https://docs.streamlit.io/develop/api-reference/text/st.help -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/help.py#L47 "View st.help source code on GitHub") | |
| --- | --- |
| st.help(obj=, \*, width="stretch") | |
| Parameters | |
| obj (any) | The object whose information should be displayed. If left unspecified, this call will display help for Streamlit itself. |
| width ("stretch" or int) | The width of the help element. This can be one of the following:   - "stretch" (default): The width of the element matches the   width of the parent container. - An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container. |

#### Example

Don't remember how to initialize a dataframe? Try this:

```
import streamlit as st
import pandas

st.help(pandas.DataFrame)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-string.streamlit.app//?utm_medium=oembed&)

Want to quickly check what data type is output by a certain function?
Try:

```
import streamlit as st

x = my_poorly_documented_function()
st.help(x)
```

Want to quickly inspect an object? No sweat:

```
class Dog:
  '''A typical dog.'''

  def __init__(self, breed, color):
    self.breed = breed
    self.color = color

  def bark(self):
    return 'Woof!'

fido = Dog("poodle", "white")

st.help(fido)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-string1.streamlit.app//?utm_medium=oembed&)

And if you're using Magic, you can get help for functions, classes,
and modules without even typing st.help:

```
import streamlit as st
import pandas

# Get help for Pandas read_csv:
pandas.read_csv

# Get help for Streamlit itself:
st
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-string2.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.text](/develop/api-reference/text/st.text)[*arrow\_forward*Next: st.html](/develop/api-reference/text/st.html)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI