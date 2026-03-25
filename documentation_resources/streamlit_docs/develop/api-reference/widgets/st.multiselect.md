<!-- Source: https://docs.streamlit.io/develop/api-reference/widgets/st.multiselect -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/widgets/multiselect.py#L260 "View st.multiselect source code on GitHub") | |
| --- | --- |
| st.multiselect(label, options, default=None, format\_func=special\_internal\_function, key=None, help=None, on\_change=None, args=None, kwargs=None, \*, max\_selections=None, placeholder=None, disabled=False, label\_visibility="visible", accept\_new\_options=False, width="stretch", bind=None) | |
| Parameters | |
| label (str) | A short label explaining to the user what this select widget is for. The label can optionally contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code, Links, and Images. Images display like icons, with a max height equal to the font height.  Unsupported Markdown elements are unwrapped so only their children (text contents) render. Common block-level Markdown (headings, lists, blockquotes) is automatically escaped and displays as literal text in labels.  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives.  For accessibility reasons, you should never set an empty label, but you can hide it with label\_visibility if needed. In the future, we may disallow empty labels by raising an exception. |
| options (Iterable) | Labels for the select options in an Iterable. This can be a list, set, or anything supported by st.dataframe. If options is dataframe-like, the first column will be used. Each label will be cast to str internally by default. |
| default (Iterable of V, V, or None) | List of default values. Can also be a single value. |
| format\_func (function) | Function to modify the display of the options. It receives the raw option as an argument and should output the label to be shown for that option. This has no impact on the return value of the command. |
| key (str, int, or None) | An optional string or integer to use as the unique key for the widget. If this is None (default), a key will be generated for the widget based on the values of the other parameters. No two widgets may have the same key. Assigning a key stabilizes the widget's identity and preserves its state across reruns even when other parameters change.  Note  Changing max\_selections or accept\_new\_options resets the widget even when a key is provided.  A key lets you read or update the widget's value via st.session\_state[key]. For more details, see [Widget behavior](https://docs.streamlit.io/develop/concepts/architecture/widget-behavior).  Additionally, if key is provided, it will be used as a CSS class name prefixed with st-key-. |
| help (str or None) | A tooltip that gets displayed next to the widget label. Streamlit only displays the tooltip when label\_visibility="visible". If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| on\_change (callable) | An optional callback invoked when this widget's value changes. |
| args (list or tuple) | An optional list or tuple of args to pass to the callback. |
| kwargs (dict) | An optional dict of kwargs to pass to the callback. |
| max\_selections (int or None) | The max selections that can be selected at a time. If this is None (default), there is no limit on the number of selections. If this is an integer, it must be positive. |
| placeholder (str or None) | A string to display when no options are selected. If this is None (default), the widget displays placeholder text based on the widget's configuration:   - "Choose options" is displayed when options are available and   accept\_new\_options=False. - "Choose or add options" is displayed when options are available   and accept\_new\_options=True. - "Add options" is displayed when no options are available and   accept\_new\_options=True. - "No options to select" is displayed when no options are available   and accept\_new\_options=False. The widget is also disabled in   this case. |
| disabled (bool) | An optional boolean that disables the multiselect widget if set to True. The default is False. |
| label\_visibility ("visible", "hidden", or "collapsed") | The visibility of the label. The default is "visible". If this is "hidden", Streamlit displays an empty spacer instead of the label, which can help keep the widget aligned with other widgets. If this is "collapsed", Streamlit displays no label or spacer. |
| accept\_new\_options (bool) | Whether the user can add selections that aren't included in options. If this is False (default), the user can only select from the items in options. If this is True, the user can enter new items that don't exist in options.  When a user enters and selects a new item, it is included in the widget's returned list as a string. The new item is not added to the widget's drop-down menu. Streamlit will use a case-insensitive match from options before adding a new item, and a new item can't be added if a case-insensitive match is already selected. The max\_selections argument is still enforced. |
| width ("stretch" or int) | The width of the multiselect widget. This can be one of the following:   - "stretch" (default): The width of the widget matches the   width of the parent container. - An integer specifying the width in pixels: The widget has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the widget matches the width   of the parent container. |
| bind ("query-params" or None) | Binding mode for syncing the widget's value with a URL query parameter. If this is None (default), the widget's value is not synced to the URL. When this is set to "query-params", changes to the widget update the URL, and the widget can be initialized or updated through a query parameter in the URL. This requires key to be set. The key is used as the query parameter name.  When the widget's value equals its default, the query parameter is removed from the URL to keep it clean. A bound query parameter can't be set or deleted through st.query\_params; it can only be programmatically changed through st.session\_state.  An empty query parameter (e.g., ?tags=) clears the widget. Invalid query parameter values are ignored and removed from the URL. Multiple selections use repeated parameters (e.g., ?tags=Red&tags=Blue). Duplicates are deduplicated. If max\_selections is set, excess values are truncated. When accept\_new\_options is True, any value is accepted. |
|  |  |
| --- | --- |
| Returns | |
| (list) | A list of the selected options.  The list contains copies of the selected options, not the originals. |

#### Examples

**Example 1: Use a basic multiselect widget**

You can declare one or more initial selections with the default
parameter.

```
import streamlit as st

options = st.multiselect(
    "What are your favorite colors?",
    ["Green", "Yellow", "Red", "Blue"],
    default=["Yellow", "Red"],
)

st.write("You selected:", options)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-multiselect.streamlit.app//?utm_medium=oembed&)

**Example 2: Let users to add new options**

To allow users to enter and select new options that aren't included in
the options list, use the accept\_new\_options parameter. To
prevent users from adding an unbounded number of new options, use the
max\_selections parameter.

```
import streamlit as st

options = st.multiselect(
    "What are your favorite cat names?",
    ["Jellybeans", "Fish Biscuit", "Madam President"],
    max_selections=5,
    accept_new_options=True,
)

st.write("You selected:", options)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-multiselect-accept-new-options.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.feedback](/develop/api-reference/widgets/st.feedback)[*arrow\_forward*Next: st.pills](/develop/api-reference/widgets/st.pills)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI