<!-- Source: https://docs.streamlit.io/develop/api-reference/status/st.error -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/alert.py#L32 "View st.error source code on GitHub") | |
| --- | --- |
| st.error(body, \*, icon=None, width="stretch") | |
| Parameters | |
| body (str) | The text to display as GitHub-flavored Markdown. Syntax information can be found at: <https://github.github.com/gfm>.  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives. |
| icon (str, None) | An optional emoji or icon to display next to the alert. If icon is None (default), no icon is displayed. If icon is a string, the following options are valid:   - A single-character emoji. For example, you can set icon="🚨"   or icon="🔥". Emoji short codes are not supported. - An icon from the Material Symbols library (rounded style) in the   format ":material/icon\_name:" where "icon\_name" is the name   of the icon in snake case.  For example, icon=":material/thumb\_up:" will display the   Thumb Up icon. Find additional icons in the [Material Symbols](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded)   font library. - "spinner": Displays a spinner as an icon. |
| width ("stretch" or int) | The width of the alert element. This can be one of the following:   - "stretch" (default): The width of the element matches the   width of the parent container. - An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container. |

#### Example

```
import streamlit as st

st.error('This is an error', icon="🚨")
```

[*arrow\_back*Previous: st.warning](/develop/api-reference/status/st.warning)[*arrow\_forward*Next: st.exception](/develop/api-reference/status/st.exception)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI