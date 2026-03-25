<!-- Source: https://docs.streamlit.io/develop/api-reference/status/st.exception -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/exception.py#L51 "View st.exception source code on GitHub") | |
| --- | --- |
| st.exception(exception, width="stretch") | |
| Parameters | |
| exception (Exception) | The exception to display. |
| width ("stretch" or int) | The width of the exception element. This can be one of the following:   - "stretch" (default): The width of the element matches the   width of the parent container. - An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container. |

#### Example

```
import streamlit as st

e = RuntimeError("This is an exception of type RuntimeError")
st.exception(e)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-status-exception.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.error](/develop/api-reference/status/st.error)[*arrow\_forward*Next: st.progress](/develop/api-reference/status/st.progress)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI