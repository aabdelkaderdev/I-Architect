<!-- Source: https://docs.streamlit.io/develop/api-reference/widgets/st.date_input -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/widgets/time_widgets.py#L1482 "View st.date_input source code on GitHub") | |
| --- | --- |
| st.date\_input(label, value="today", min\_value=None, max\_value=None, key=None, help=None, on\_change=None, args=None, kwargs=None, \*, format="YYYY/MM/DD", disabled=False, label\_visibility="visible", width="stretch", bind=None) | |
| Parameters | |
| label (str) | A short label explaining to the user what this date input is for. The label can optionally contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code, Links, and Images. Images display like icons, with a max height equal to the font height.  Unsupported Markdown elements are unwrapped so only their children (text contents) render. Common block-level Markdown (headings, lists, blockquotes) is automatically escaped and displays as literal text in labels.  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives.  For accessibility reasons, you should never set an empty label, but you can hide it with label\_visibility if needed. In the future, we may disallow empty labels by raising an exception. |
| value ("today", datetime.date, datetime.datetime, str, list/tuple of these, or None) | The value of this widget when it first renders. This can be one of the following:   - "today" (default): The widget initializes with the current date. - A datetime.date or datetime.datetime object: The widget   initializes with the given date, ignoring any time if included. - An ISO-formatted date (YYYY-MM-DD) or datetime   (YYYY-MM-DD hh:mm:ss) string: The widget initializes with the   given date, ignoring any time if included. - A list or tuple with up to two of the above: The widget will   initialize with the given date interval and return a tuple of the   selected interval. You can pass an empty list to initialize the   widget with an empty interval or a list with one value to   initialize only the beginning date of the iterval. - None: The widget initializes with no date and returns   None until the user selects a date. |
| min\_value ("today", datetime.date, datetime.datetime, str, or None) | The minimum selectable date. This can be any of the date types accepted by value, except list or tuple.  If this is None (default), the minimum selectable date is ten years before the initial value. If the initial value is an interval, the minimum selectable date is ten years before the start date of the interval. If no initial value is set, the minimum selectable date is ten years before today. |
| max\_value ("today", datetime.date, datetime.datetime, str, or None) | The maximum selectable date. This can be any of the date types accepted by value, except list or tuple.  If this is None (default), the maximum selectable date is ten years after the initial value. If the initial value is an interval, the maximum selectable date is ten years after the end date of the interval. If no initial value is set, the maximum selectable date is ten years after today. |
| key (str, int, or None) | An optional string or integer to use as the unique key for the widget. If this is None (default), a key will be generated for the widget based on the values of the other parameters. No two widgets may have the same key. Assigning a key stabilizes the widget's identity and preserves its state across reruns even when other parameters change.  Note  Changing format resets the widget even when a key is provided.  A key lets you read or update the widget's value via st.session\_state[key]. For more details, see [Widget behavior](https://docs.streamlit.io/develop/concepts/architecture/widget-behavior).  Additionally, if key is provided, it will be used as a CSS class name prefixed with st-key-. |
| help (str or None) | A tooltip that gets displayed next to the widget label. Streamlit only displays the tooltip when label\_visibility="visible". If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| on\_change (callable) | An optional callback invoked when this date\_input's value changes. |
| args (list or tuple) | An optional list or tuple of args to pass to the callback. |
| kwargs (dict) | An optional dict of kwargs to pass to the callback. |
| format (str) | A format string controlling how the interface should display dates. Supports "YYYY/MM/DD" (default), "DD/MM/YYYY", or "MM/DD/YYYY". You may also use a period (.) or hyphen (-) as separators. |
| disabled (bool) | An optional boolean that disables the date input if set to True. The default is False. |
| label\_visibility ("visible", "hidden", or "collapsed") | The visibility of the label. The default is "visible". If this is "hidden", Streamlit displays an empty spacer instead of the label, which can help keep the widget aligned with other widgets. If this is "collapsed", Streamlit displays no label or spacer. |
| width ("stretch" or int) | The width of the date input widget. This can be one of the following:   - "stretch" (default): The width of the widget matches the   width of the parent container. - An integer specifying the width in pixels: The widget has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the widget matches the width   of the parent container. |
| bind ("query-params" or None) | Binding mode for syncing the widget's value with a URL query parameter. If this is None (default), the widget's value is not synced to the URL. When this is set to "query-params", changes to the widget update the URL, and the widget can be initialized or updated through a query parameter in the URL. This requires key to be set. The key is used as the query parameter name.  When the widget's value equals its default, the query parameter is removed from the URL to keep it clean. A bound query parameter can't be set or deleted through st.query\_params; it can only be programmatically changed through st.session\_state.  Dates use ISO 8601 format (YYYY-MM-DD) in the URL. Invalid query parameter values are ignored and removed from the URL. If value is None, an empty query parameter (e.g., ?vacation=) clears the widget. Date ranges use repeated parameters (e.g., ?vacation=2025-01-01&vacation=2025-01-31). |
|  |  |
| --- | --- |
| Returns | |
| (datetime.date or a tuple with 0-2 dates or None) | The current value of the date input widget or None if no date has been selected. |

#### Examples

**Example 1: Basic usage**

```
import datetime
import streamlit as st

d = st.date_input("When's your birthday", datetime.date(2019, 7, 6))
st.write("Your birthday is:", d)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-date-input.streamlit.app//?utm_medium=oembed&)

**Example 2: Date range**

```
import datetime
import streamlit as st

today = datetime.datetime.now()
next_year = today.year + 1
jan_1 = datetime.date(next_year, 1, 1)
dec_31 = datetime.date(next_year, 12, 31)

d = st.date_input(
    "Select your vacation for next year",
    (jan_1, datetime.date(next_year, 1, 7)),
    jan_1,
    dec_31,
    format="MM.DD.YYYY",
)
d
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-date-input1.streamlit.app//?utm_medium=oembed&)

**Example 3: Empty initial value**

To initialize an empty date input, use None as the value:

```
import datetime
import streamlit as st

d = st.date_input("When's your birthday", value=None)
st.write("Your birthday is:", d)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-date-input-empty.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.slider](/develop/api-reference/widgets/st.slider)[*arrow\_forward*Next: st.datetime\_input](/develop/api-reference/widgets/st.datetime_input)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI