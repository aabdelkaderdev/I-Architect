<!-- Source: https://docs.streamlit.io/develop/api-reference/layout/st.expander -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/layouts.py#L960 "View st.expander source code on GitHub") | |
| --- | --- |
| st.expander(label, expanded=False, \*, key=None, icon=None, width="stretch", on\_change="ignore", args=None, kwargs=None) | |
| Parameters | |
| label (str) | A string to use as the header for the expander. The label can optionally contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code, Links, and Images. Images display like icons, with a max height equal to the font height.  Unsupported Markdown elements are unwrapped so only their children (text contents) render. Common block-level Markdown (headings, lists, blockquotes) is automatically escaped and displays as literal text in labels.  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives. |
| expanded (bool) | If True, initializes the expander in "expanded" state. Defaults to False (collapsed). |
| key (str, int, or None) | An optional string or integer to use as the unique key for the widget. If this is None (default), a key will be generated for the widget based on the values of the other parameters. No two widgets may have the same key.  When on\_change is set to "rerun" or a callable, setting a key lets you read or update the expanded state via st.session\_state[key]. For more details, see [Widget behavior](https://docs.streamlit.io/develop/concepts/architecture/widget-behavior). |
| icon (str, None) | An optional emoji or icon to display next to the expander label. If icon is None (default), no icon is displayed. If icon is a string, the following options are valid:   - A single-character emoji. For example, you can set icon="🚨"   or icon="🔥". Emoji short codes are not supported. - An icon from the Material Symbols library (rounded style) in the   format ":material/icon\_name:" where "icon\_name" is the name   of the icon in snake case.  For example, icon=":material/thumb\_up:" will display the   Thumb Up icon. Find additional icons in the [Material Symbols](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded)    font library. - "spinner": Displays a spinner as an icon. |
| width ("stretch" or int) | The width of the expander container. This can be one of the following:   - "stretch" (default): The width of the container matches the   width of the parent container. - An integer specifying the width in pixels: The container has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the container matches the width   of the parent container. |
| on\_change ("ignore", "rerun", or callable) | How the expander should respond when the user expands or collapses it. This controls whether the expander tracks state and triggers reruns. on\_change can be one of the following:   - "ignore" (default): The expander doesn't track state. All   expander content runs regardless of whether the expander is open   or closed. The .open attribute of the expander container   returns None. - "rerun": The expander tracks state. Streamlit reruns the app   when the user expands or collapses the expander. The .open   attribute of the expander container returns the current state,   which is True if the expander is open and False if it's   closed. This lets you skip expensive work when the expander is   closed. - A callable: The expander tracks state. Streamlit executes the   callable as a callback function and reruns the app when the user   expands or collapses the expander. The .open attribute of the   expander container returns its state like when   on\_change="rerun". If you need to access the current state   inside your callback, fetch it through Session State.   When the expander tracks state, it can't be used inside Streamlit cache-decorated functions. |
| args (list or tuple or None) | An optional list or tuple of args to pass to the on\_change callback. |
| kwargs (dict or None) | An optional dict of kwargs to pass to the on\_change callback. |
|  |  |
| --- | --- |
| Returns | |
| (ExpanderContainer) | An ExpanderContainer object with an .open property to return the current state of the expander if the expander tracks state. |

#### Examples

**Example 1: Use context management**
You can use the with notation to insert any element into an expander

```
import streamlit as st

st.bar_chart({"data": [1, 5, 2, 6, 2, 1]})

with st.expander("See explanation"):
    st.write('''
        The chart above shows some numbers I picked for you.
        I rolled actual dice for these, so they're *guaranteed* to
        be random.
    ''')
    st.image("https://static.streamlit.io/examples/dice.jpg")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-expander.streamlit.app//?utm_medium=oembed&)

**Example 2: Call methods directly**

You can call methods directly on the returned object:

```
import streamlit as st

st.bar_chart({"data": [1, 5, 2, 6, 2, 1]})

expander = st.expander("See explanation")
expander.write('''
    The chart above shows some numbers I picked for you.
    I rolled actual dice for these, so they're *guaranteed* to
    be random.
''')
expander.image("https://static.streamlit.io/examples/dice.jpg")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-expander.streamlit.app//?utm_medium=oembed&)

**Example 3: Programmatically control the expander state**

You can use a key to programmatically control the expander state or
access the state in callbacks. You must set the on\_change parameter
for the expander to track state.

```
import streamlit as st

def toggle_expander():
    st.session_state.summary = not st.session_state.summary

def on_expander_change():
    if st.session_state.summary:
        st.toast("You opened the expander.")
    else:
        st.toast("You closed the expander.")

with st.expander("Open expander", on_change=on_expander_change, key="summary"):
    st.write("This is the expander")

st.button("Toggle expander", on_click=toggle_expander)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-expander-callback.streamlit.app//?utm_medium=oembed&)

|  |  |
| --- | --- |
| Attributes | |
| open (bool or None) | Whether the expander is open. This is True if the expander is open and False if it's collapsed, or None if state tracking isn't enabled. |

#### Examples

**Example 1: Lazy loading content**

```
import streamlit as st
import time

summary = st.expander("Summary", on_change="rerun")

if summary.open:
    with summary:
        with st.spinner("Loading summary..."):
            time.sleep(2)
        st.write("This is the summary")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-expander-lazy-load.streamlit.app//?utm_medium=oembed&)

**Example 2: Conditionally render content outside of the expander**

```
import streamlit as st

summary = st.expander("Summary", on_change="rerun")
with summary:
    st.write("This is the summary")

st.write(
    f"The expander is {':green[open]' if summary.open else ':red[closed]'}."
)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-expander-conditional-outside.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.empty](/develop/api-reference/layout/st.empty)[*arrow\_forward*Next: st.form](https://docs.streamlit.io/develop/api-reference/execution-flow/st.form)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI