<!-- Source: https://docs.streamlit.io/develop/api-reference/widgets/st.datetime_input -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/widgets/time_widgets.py#L1032 "View st.datetime_input source code on GitHub") | |
| --- | --- |
| st.datetime\_input(label, value="now", min\_value=None, max\_value=None, \*, key=None, help=None, on\_change=None, args=None, kwargs=None, format="YYYY/MM/DD", step=0:15:00, disabled=False, label\_visibility="visible", width="stretch", bind=None) | |
| Parameters | |
| label (str) | A short label explaining to the user what this datetime input is for. The label can optionally contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code, Links, and Images. Images display like icons, with a max height equal to the font height.  Unsupported Markdown elements are unwrapped so only their children (text contents) render. Common block-level Markdown (headings, lists, blockquotes) is automatically escaped and displays as literal text in labels.  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives.  For accessibility reasons, you should never set an empty label, but you can hide it with label\_visibility if needed. In the future, we may disallow empty labels by raising an exception. |
| value ("now", datetime.datetime, datetime.date, datetime.time, str, or None) | The value of this widget when it first renders. This can be one of the following:   - "now" (default): The widget initializes with the current date and time. - A datetime.datetime object: The widget initializes with the given   datetime, stripping any timezone information. - A datetime.date object: The widget initializes with the given date   at 00:00. - A datetime.time object: The widget initializes with today's date   and the provided time. - An ISO-formatted datetime (YYYY-MM-DD hh:mm[:ss]) or date/time   string: The widget initializes with the parsed value. - None: The widget initializes with no value and returns None   until the user selects a datetime. |
| min\_value ("now", datetime.datetime, datetime.date, datetime.time, str, or None) | The minimum selectable datetime. This can be any of the datetime types accepted by value.  If this is None (default), the minimum selectable datetime is ten years before the initial value. If no initial value is set, the minimum selectable datetime is ten years before today at 00:00. |
| max\_value ("now", datetime.datetime, datetime.date, datetime.time, str, or None) | The maximum selectable datetime. This can be any of the datetime types accepted by value.  If this is None (default), the maximum selectable datetime is ten years after the initial value. If no initial value is set, the maximum selectable datetime is ten years after today at 23:59. |
| key (str, int, or None) | An optional string or integer to use as the unique key for the widget. If this is None (default), a key will be generated for the widget based on the values of the other parameters. No two widgets may have the same key. Assigning a key stabilizes the widget's identity and preserves its state across reruns even when other parameters change.  Note  Changing format or step resets the widget even when a key is provided.  A key lets you read or update the widget's value via st.session\_state[key]. For more details, see [Widget behavior](https://docs.streamlit.io/develop/concepts/architecture/widget-behavior).  Additionally, if key is provided, it will be used as a CSS class name prefixed with st-key-. |
| help (str or None) | A tooltip that gets displayed next to the widget label. Streamlit only displays the tooltip when label\_visibility="visible". If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| on\_change (callable) | An optional callback invoked when this datetime\_input's value changes. |
| args (list or tuple) | An optional list or tuple of args to pass to the callback. |
| kwargs (dict) | An optional dict of kwargs to pass to the callback. |
| format (str) | A format string controlling how the interface displays dates. Supports "YYYY/MM/DD" (default), "DD/MM/YYYY", or "MM/DD/YYYY". You may also use a period (.) or hyphen (-) as separators. This doesn't affect the time format. |
| step (int or timedelta) | The stepping interval in seconds. This defaults to 900 (15 minutes). You can also pass a datetime.timedelta object. The value must be between 60 seconds and 23 hours. |
| disabled (bool) | An optional boolean that disables the widget if set to True. The default is False. |
| label\_visibility ("visible", "hidden", or "collapsed") | The visibility of the label. The default is "visible". If this is "hidden", Streamlit displays an empty spacer instead of the label, which can help keep the widget aligned with other widgets. If this is "collapsed", Streamlit displays no label or spacer. |
| width ("stretch" or int) | The width of the widget. This can be one of the following:   - "stretch" (default): The width of the widget matches the width   of the parent container. - An integer specifying the width in pixels: The widget has a fixed   width. If the specified width is greater than the width of the   parent container, the widget matches the container width. |
| bind ("query-params" or None) | Binding mode for syncing the widget's value with a URL query parameter. If this is None (default), the widget's value is not synced to the URL. When this is set to "query-params", changes to the widget update the URL, and the widget can be initialized or updated through a query parameter in the URL. This requires key to be set. The key is used as the query parameter name.  When the widget's value equals its default, the query parameter is removed from the URL to keep it clean. A bound query parameter can't be set or deleted through st.query\_params; it can only be programmatically changed through st.session\_state.  Datetimes use ISO 8601 format (YYYY-MM-DDThh:mm) in the URL. Invalid query parameter values are ignored and removed from the URL. If value is None, an empty query parameter (e.g., ?my\_key=) clears the widget. |
|  |  |
| --- | --- |
| Returns | |
| (datetime.datetime or None) | The current value of the datetime input widget (without timezone) or None if no value has been selected. |

#### Examples

**Example 1: Basic usage**

```
import datetime
import streamlit as st

event_time = st.datetime_input(
    "Schedule your event",
    datetime.datetime(2025, 11, 19, 16, 45),
)
st.write("Event scheduled for", event_time)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-datetime-input.streamlit.app//?utm_medium=oembed&)

**Example 2: Empty initial value**

To initialize an empty datetime input, use None as the value:

```
import datetime
import streamlit as st

event_time = st.datetime_input("Schedule your event", value=None)
st.write("Event scheduled for", event_time)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-datetime-input-empty.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.date\_input](/develop/api-reference/widgets/st.date_input)[*arrow\_forward*Next: st.time\_input](/develop/api-reference/widgets/st.time_input)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI