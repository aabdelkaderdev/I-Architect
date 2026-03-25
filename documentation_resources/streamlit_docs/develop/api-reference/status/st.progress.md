<!-- Source: https://docs.streamlit.io/develop/api-reference/status/st.progress -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/progress.py#L92 "View st.progress source code on GitHub") | |
| --- | --- |
| st.progress(value, text=None, width="stretch") | |
| Parameters | |
| value (int or float) | 0 <= value <= 100 for int  0.0 <= value <= 1.0 for float |
| text (str or None) | A message to display above the progress bar. The text can optionally contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code, Links, and Images. Images display like icons, with a max height equal to the font height.  Unsupported Markdown elements are unwrapped so only their children (text contents) render. Common block-level Markdown (headings, lists, blockquotes) is automatically escaped and displays as literal text in labels.  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives. |
| width ("stretch" or int) | The width of the progress element. This can be one of the following:   - "stretch" (default): The width of the element matches the   width of the parent container. - An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container. |

#### Example

Here is an example of a progress bar increasing over time and disappearing when it reaches completion:

```
import streamlit as st
import time

progress_text = "Operation in progress. Please wait."
my_bar = st.progress(0, text=progress_text)

for percent_complete in range(100):
    time.sleep(0.01)
    my_bar.progress(percent_complete + 1, text=progress_text)
time.sleep(1)
my_bar.empty()

st.button("Rerun")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-status-progress.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.exception](/develop/api-reference/status/st.exception)[*arrow\_forward*Next: st.spinner](/develop/api-reference/status/st.spinner)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI