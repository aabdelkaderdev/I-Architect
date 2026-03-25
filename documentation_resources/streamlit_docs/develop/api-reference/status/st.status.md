<!-- Source: https://docs.streamlit.io/develop/api-reference/status/st.status -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/layouts.py#L1625 "View st.status source code on GitHub") | |
| --- | --- |
| st.status(label, \*, expanded=False, state="running", width="stretch") | |
| Parameters | |
| label (str) | The initial label of the status container. The label can optionally contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code, Links, and Images. Images display like icons, with a max height equal to the font height.  Unsupported Markdown elements are unwrapped so only their children (text contents) render. Common block-level Markdown (headings, lists, blockquotes) is automatically escaped and displays as literal text in labels.  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives. |
| expanded (bool) | If True, initializes the status container in "expanded" state. Defaults to False (collapsed). |
| state ("running", "complete", or "error") | The initial state of the status container which determines which icon is shown:   - running (default): A spinner icon is shown. - complete: A checkmark icon is shown. - error: An error icon is shown. |
| width ("stretch" or int) | The width of the status container. This can be one of the following:   - "stretch" (default): The width of the container matches the   width of the parent container. - An integer specifying the width in pixels: The container has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the container matches the width   of the parent container. |
|  |  |
| --- | --- |
| Returns | |
| (StatusContainer) | A mutable status container that can hold multiple elements. The label, state, and expanded state can be updated after creation via .update(). |

#### Examples

You can use the with notation to insert any element into an status container:

```
import time
import streamlit as st

with st.status("Downloading data..."):
    st.write("Searching for data...")
    time.sleep(2)
    st.write("Found URL.")
    time.sleep(1)
    st.write("Downloading data...")
    time.sleep(1)

st.button("Rerun")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-status.streamlit.app//?utm_medium=oembed&)

You can also use .update() on the container to change the label, state,
or expanded state:

```
import time
import streamlit as st

with st.status("Downloading data...", expanded=True) as status:
    st.write("Searching for data...")
    time.sleep(2)
    st.write("Found URL.")
    time.sleep(1)
    st.write("Downloading data...")
    time.sleep(1)
    status.update(
        label="Download complete!", state="complete", expanded=False
    )

st.button("Rerun")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-status-update.streamlit.app//?utm_medium=oembed&)

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/lib/mutable_status_container.py#L108 "View st.update source code on GitHub") | |
| --- | --- |
| StatusContainer.update(\*, label=None, expanded=None, state=None) | |
| Parameters | |
| label (str or None) | A new label of the status container. If None, the label is not changed. |
| expanded (bool or None) | The new expanded state of the status container. If None, the expanded state is not changed. |
| state ("running", "complete", "error", or None) | The new state of the status container. This mainly changes the icon. If None, the state is not changed. |

[*arrow\_back*Previous: st.spinner](/develop/api-reference/status/st.spinner)[*arrow\_forward*Next: st.toast](/develop/api-reference/status/st.toast)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI