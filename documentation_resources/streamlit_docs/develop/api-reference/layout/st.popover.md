<!-- Source: https://docs.streamlit.io/develop/api-reference/layout/st.popover -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/layouts.py#L1261 "View st.popover source code on GitHub") | |
| --- | --- |
| st.popover(label, \*, type="secondary", help=None, icon=None, disabled=False, use\_container\_width=None, width="content", key=None, on\_change="ignore", args=None, kwargs=None) | |
| Parameters | |
| label (str) | The label of the button that opens the popover container. The label can optionally contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code, Links, and Images. Images display like icons, with a max height equal to the font height.  Unsupported Markdown elements are unwrapped so only their children (text contents) render. Common block-level Markdown (headings, lists, blockquotes) is automatically escaped and displays as literal text in labels.  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives. |
| help (str or None) | A tooltip that gets displayed when the popover button is hovered over. If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| type ("primary", "secondary", or "tertiary") | An optional string that specifies the button type. This can be one of the following:   - "primary": The button's background is the app's primary color   for additional emphasis. - "secondary" (default): The button's background coordinates   with the app's background color for normal emphasis. - "tertiary": The button is plain text without a border or   background for subtlety. |
| icon (str) | An optional emoji or icon to display next to the button label. If icon is None (default), no icon is displayed. If icon is a string, the following options are valid:   - A single-character emoji. For example, you can set icon="🚨"   or icon="🔥". Emoji short codes are not supported. - An icon from the Material Symbols library (rounded style) in the   format ":material/icon\_name:" where "icon\_name" is the name   of the icon in snake case.  For example, icon=":material/thumb\_up:" will display the   Thumb Up icon. Find additional icons in the [Material Symbols](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded)    font library. - "spinner": Displays a spinner as an icon. |
| disabled (bool) | An optional boolean that disables the popover button if set to True. The default is False. |
| use\_container\_width (bool) | *delete* use\_container\_width is deprecated and will be removed in a future release. For use\_container\_width=True, use width="stretch". For use\_container\_width=False, use width="content".  Whether to expand the button's width to fill its parent container. If use\_container\_width is False (default), Streamlit sizes the button to fit its content. If use\_container\_width is True, the width of the button matches its parent container.  In both cases, if the content of the button is wider than the parent container, the content will line wrap.  The popover container's minimum width matches the width of its button. The popover container may be wider than its button to fit the container's content. |
| width (int, "stretch", or "content") | The width of the button. This can be one of the following:   - "content" (default): The width of the button matches the   width of its content, but doesn't exceed the width of the parent   container. - "stretch": The width of the button matches the width of the   parent container. - An integer specifying the width in pixels: The button has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the button matches the width   of the parent container.   The popover container's minimum width matches the width of its button. The popover container may be wider than its button to fit the container's contents. |
| key (str, int, or None) | An optional string or integer to use as the unique key for the widget. If this is None (default), a key will be generated for the widget based on the values of the other parameters. No two widgets may have the same key.  When on\_change is set to "rerun" or a callable, setting a key lets you read or update the open/closed state via st.session\_state[key]. For more details, see [Widget behavior](https://docs.streamlit.io/develop/concepts/architecture/widget-behavior). |
| on\_change ("ignore", "rerun", or callable) | How the popover should respond when the user opens or closes it. This controls whether the popover tracks state and triggers reruns. on\_change can be one of the following values:   - "ignore" (default): The popover doesn't track state. All   popover content runs regardless of whether the popover is open or   closed. The .open attribute of the popover container returns   None. - "rerun": The popover tracks state. Streamlit reruns the app   when the user opens or closes the popover. The .open   attribute of the popover container returns the current state,   which is True if the popover is open and False if it's   closed. This lets you skip expensive work when the popover is   closed. - A callable: The popover tracks state. Streamlit executes the   callable as a callback function and reruns the app when the user   opens or closes the popover. The .open attribute of the   popover container returns its state like when   on\_change="rerun". If you need to access the current state   inside your callback, fetch it through Session State.   When the popover tracks state, it can't be used inside Streamlit cache-decorated functions. |
| args (list or tuple or None) | An optional list or tuple of args to pass to the on\_change callback. |
| kwargs (dict or None) | An optional dict of kwargs to pass to the on\_change callback. |
|  |  |
| --- | --- |
| Returns | |
| (PopoverContainer) | A PopoverContainer object with an .open property to return the current state of the popover if the popover tracks state. |

#### Examples

**Example 1: Use context management**
You can use the with notation to insert any element into a popover:

```
import streamlit as st

with st.popover("Open popover"):
    st.markdown("Hello World 👋")
    name = st.text_input("What's your name?")

st.write("Your name:", name)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-popover.streamlit.app//?utm_medium=oembed&)

**Example 2: Call methods directly**

You can call methods directly on the returned object:

```
import streamlit as st

popover = st.popover("Filter items")
red = popover.checkbox("Show red items.", True)
blue = popover.checkbox("Show blue items.", True)

if red:
    st.write(":red[This is a red item.]")
if blue:
    st.write(":blue[This is a blue item.]")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-popover2.streamlit.app//?utm_medium=oembed&)

**Example 3: Programmatically control the popover state**

You can use a key to programmatically control the popover state or
access the state in callbacks. You must set the on\_change parameter
for the popover to track state.

```
import streamlit as st

def toggle_popover():
    st.session_state.drawer = not st.session_state.drawer

def on_popover_change():
    if st.session_state.drawer:
        st.toast("You opened the popover.")
    else:
        st.toast("You closed the popover.")

with st.popover("Open popover", on_change=on_popover_change, key="drawer"):
    st.write("This is the popover")
    st.button("Close popover", on_click=toggle_popover)

st.button("Open popover", on_click=toggle_popover)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-popover-callback.streamlit.app//?utm_medium=oembed&)

|  |  |
| --- | --- |
| Attributes | |
| open (bool or None) | Whether the popover is open. This is True if the popover is open and False if it's closed, or None if state tracking isn't enabled. |

#### Examples

**Example 1: Lazy loading content**

```
import streamlit as st
import time

drawer = st.popover("Open popover", on_change="rerun")
with drawer:
    if drawer.open:
        with st.spinner("Loading popover..."):
            time.sleep(2)
        st.write("This is the popover")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-popover-lazy-load.streamlit.app//?utm_medium=oembed&)

**Example 2: Conditionally render content outside of the popover**

```
import streamlit as st

drawer = st.popover("Open popover", on_change="rerun")
with drawer:
    st.write("This is the popover")

st.space("large")
st.write(f"The popover is {':green[open]' if drawer.open else ':red[closed]'}.")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-popover-conditional-outside.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.form](https://docs.streamlit.io/develop/api-reference/execution-flow/st.form)[*arrow\_forward*Next: st.sidebar](/develop/api-reference/layout/st.sidebar)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI