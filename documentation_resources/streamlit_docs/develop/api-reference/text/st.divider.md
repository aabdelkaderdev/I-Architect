<!-- Source: https://docs.streamlit.io/develop/api-reference/text/st.divider -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/markdown.py#L377 "View st.divider source code on GitHub") | |
| --- | --- |
| st.divider(\*, width="stretch") | |
| Parameters | |
| width ("stretch" or int) | The width of the divider element. This can be one of the following:   - "stretch" (default): The width of the element matches the   width of the parent container. - An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container. |

#### Example

```
import streamlit as st

st.divider()
```

Here's what it looks like in action when you have multiple elements in the app:

```
import streamlit as st

st.write("This is some text.")

st.slider("This is a slider", 0, 100, (25, 75))

st.divider()  # 👈 Draws a horizontal rule

st.write("This text is between the horizontal rules.")

st.divider()  # 👈 Another horizontal rule
```

[*arrow\_back*Previous: st.code](/develop/api-reference/text/st.code)[*arrow\_forward*Next: st.echo](/develop/api-reference/text/st.echo)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI