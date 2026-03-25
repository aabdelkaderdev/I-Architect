<!-- Source: https://docs.streamlit.io/develop/api-reference/layout/st.space -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/space.py#L32 "View st.space source code on GitHub") | |
| --- | --- |
| st.space(size="small") | |
| Parameters | |
| size ("xxsmall", "xsmall", "small", "medium", "large", "xlarge", "xxlarge", "stretch", or int) | The size of the space. This can be one of the following values:   - "xxsmall": 0.25rem, matching the "xxsmall" gap in   st.container and st.columns. - "xsmall": 0.5rem, matching the "xsmall" gap in   st.container and st.columns. - "small" (default): 0.75rem, which is the height of a widget   label. This is useful for aligning buttons with labeled widgets. - "medium": 2.5rem, which is the height of a button or   (unlabeled) input field. - "large": 4.25rem, which is the height of a labeled input   field or unlabeled media widget, like st.file\_uploader. - "xlarge": 6rem, matching the "xlarge" gap in   st.container and st.columns. - "xxlarge": 8rem, matching the "xxlarge" gap in   st.container and st.columns. - "stretch": Expands to fill remaining space in the container. - An integer: Fixed size in pixels. |

#### Examples

**Example 1: Use vertical space to align elements**

Use small spaces to replace label heights. Use medium spaces to replace
two label heights or a button.

```
import streamlit as st

left, middle, right = st.columns(3)

left.space("medium")
left.button("Left button", width="stretch")

middle.space("small")
middle.text_input("Middle input")

right.audio_input("Right uploader")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-space-vertical.streamlit.app//?utm_medium=oembed&)

**Example 2: Add horizontal space in a container**

Use stretch space to float elements left and right.

```
import streamlit as st

with st.container(horizontal=True):
    st.button("Left")
    st.space("stretch")
    st.button("Right")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-space-horizontal.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.sidebar](/develop/api-reference/layout/st.sidebar)[*arrow\_forward*Next: st.tabs](/develop/api-reference/layout/st.tabs)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI