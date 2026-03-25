<!-- Source: https://docs.streamlit.io/develop/api-reference/widgets/st.selectbox -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/widgets/selectbox.py#L298 "View st.selectbox source code on GitHub") | |
| --- | --- |
| st.selectbox(label, options, index=0, format\_func=special\_internal\_function, key=None, help=None, on\_change=None, args=None, kwargs=None, \*, placeholder=None, disabled=False, label\_visibility="visible", accept\_new\_options=False, width="stretch", bind=None) | |
| Parameters | |
| label (str) | A short label explaining to the user what this select widget is for. The label can optionally contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code, Links, and Images. Images display like icons, with a max height equal to the font height.  Unsupported Markdown elements are unwrapped so only their children (text contents) render. Common block-level Markdown (headings, lists, blockquotes) is automatically escaped and displays as literal text in labels.  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives.  For accessibility reasons, you should never set an empty label, but you can hide it with label\_visibility if needed. In the future, we may disallow empty labels by raising an exception. |
| options (Iterable) | Labels for the select options in an Iterable. This can be a list, set, or anything supported by st.dataframe. If options is dataframe-like, the first column will be used. Each label will be cast to str internally by default. |
| index (int or None) | The index of the preselected option on first render. If None, will initialize empty and return None until the user selects an option. Defaults to 0 (the first option). |
| format\_func (function) | Function to modify the display of the options. It receives the raw option as an argument and should output the label to be shown for that option. This has no impact on the return value of the command. |
| key (str, int, or None) | An optional string or integer to use as the unique key for the widget. If this is None (default), a key will be generated for the widget based on the values of the other parameters. No two widgets may have the same key. Assigning a key stabilizes the widget's identity and preserves its state across reruns even when other parameters change.  Note  Changing accept\_new\_options resets the widget even when a key is provided.  A key lets you read or update the widget's value via st.session\_state[key]. For more details, see [Widget behavior](https://docs.streamlit.io/develop/concepts/architecture/widget-behavior).  Additionally, if key is provided, it will be used as a CSS class name prefixed with st-key-. |
| help (str or None) | A tooltip that gets displayed next to the widget label. Streamlit only displays the tooltip when label\_visibility="visible". If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| on\_change (callable) | An optional callback invoked when this selectbox's value changes. |
| args (list or tuple) | An optional list or tuple of args to pass to the callback. |
| kwargs (dict) | An optional dict of kwargs to pass to the callback. |
| placeholder (str or None) | A string to display when no options are selected. If this is None (default), the widget displays placeholder text based on the widget's configuration:   - "Choose an option" is displayed when options are available and   accept\_new\_options=False. - "Choose or add an option" is displayed when options are available   and accept\_new\_options=True. - "Add an option" is displayed when no options are available and   accept\_new\_options=True. - "No options to select" is displayed when no options are available   and accept\_new\_options=False. The widget is also disabled in   this case. |
| disabled (bool) | An optional boolean that disables the selectbox if set to True. The default is False. |
| label\_visibility ("visible", "hidden", or "collapsed") | The visibility of the label. The default is "visible". If this is "hidden", Streamlit displays an empty spacer instead of the label, which can help keep the widget aligned with other widgets. If this is "collapsed", Streamlit displays no label or spacer. |
| accept\_new\_options (bool) | Whether the user can add a selection that isn't included in options. If this is False (default), the user can only select from the items in options. If this is True, the user can enter a new item that doesn't exist in options.  When a user enters a new item, it is returned by the widget as a string. The new item is not added to the widget's drop-down menu. Streamlit will use a case-insensitive match from options before adding a new item. |
| width ("stretch" or int) | The width of the selectbox widget. This can be one of the following:   - "stretch" (default): The width of the widget matches the   width of the parent container. - An integer specifying the width in pixels: The widget has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the widget matches the width   of the parent container. |
| bind ("query-params" or None) | Binding mode for syncing the widget's value with a URL query parameter. If this is None (default), the widget's value is not synced to the URL. When this is set to "query-params", changes to the widget update the URL, and the widget can be initialized or updated through a query parameter in the URL. This requires key to be set. The key is used as the query parameter name.  When the widget's value equals its default, the query parameter is removed from the URL to keep it clean. A bound query parameter can't be set or deleted through st.query\_params; it can only be programmatically changed through st.session\_state.  Invalid query parameter values are ignored and removed from the URL. If index is None, an empty query parameter (e.g., ?my\_key=) clears the widget. |
|  |  |
| --- | --- |
| Returns | |
| (any) | The selected option or None if no option is selected.  This is a copy of the selected option, not the original. |

#### Examples

**Example 1: Use a basic selectbox widget**

If no index is provided, the first option is selected by default.

```
import streamlit as st

option = st.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone"),
)

st.write("You selected:", option)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-selectbox.streamlit.app//?utm_medium=oembed&)

**Example 2: Use a selectbox widget with no initial selection**

To initialize an empty selectbox, use None as the index value.

```
import streamlit as st

option = st.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone"),
    index=None,
    placeholder="Select contact method...",
)

st.write("You selected:", option)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-selectbox-empty.streamlit.app//?utm_medium=oembed&)

**Example 3: Let users add a new option**

To allow users to add a new option that isn't included in the
options list, use the accept\_new\_options=True parameter. You
can also customize the placeholder text.

```
import streamlit as st

option = st.selectbox(
    "Default email",
    ["foo@example.com", "bar@example.com", "baz@example.com"],
    index=None,
    placeholder="Select a saved email or enter a new one",
    accept_new_options=True,
)

st.write("You selected:", option)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-selectbox-accept-new-options.streamlit.app//?utm_medium=oembed&)

  

Select widgets can customize how to hide their labels with the `label_visibility` parameter. If "hidden", the label doesn’t show but there is still empty space for it above the widget (equivalent to `label=""`). If "collapsed", both the label and the space are removed. Default is "visible". Select widgets can also be disabled with the `disabled` parameter:

```
import streamlit as st

# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

col1, col2 = st.columns(2)

with col1:
    st.checkbox("Disable selectbox widget", key="disabled")
    st.radio(
        "Set selectbox label visibility 👉",
        key="visibility",
        options=["visible", "hidden", "collapsed"],
    )

with col2:
    option = st.selectbox(
        "How would you like to be contacted?",
        ("Email", "Home phone", "Mobile phone"),
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
    )
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-selectbox1.streamlit.app/?utm_medium=oembed)

[*arrow\_back*Previous: st.segmented\_control](/develop/api-reference/widgets/st.segmented_control)[*arrow\_forward*Next: st.select\_slider](/develop/api-reference/widgets/st.select_slider)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI