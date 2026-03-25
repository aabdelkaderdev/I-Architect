<!-- Source: https://docs.streamlit.io/develop/api-reference/widgets/st.slider -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/widgets/slider.py#L455 "View st.slider source code on GitHub") | |
| --- | --- |
| st.slider(label, min\_value=None, max\_value=None, value=None, step=None, format=None, key=None, help=None, on\_change=None, args=None, kwargs=None, \*, disabled=False, label\_visibility="visible", width="stretch", bind=None) | |
| Parameters | |
| label (str) | A short label explaining to the user what this slider is for. The label can optionally contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code, Links, and Images. Images display like icons, with a max height equal to the font height.  Unsupported Markdown elements are unwrapped so only their children (text contents) render. Common block-level Markdown (headings, lists, blockquotes) is automatically escaped and displays as literal text in labels.  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives.  For accessibility reasons, you should never set an empty label, but you can hide it with label\_visibility if needed. In the future, we may disallow empty labels by raising an exception. |
| min\_value (a supported type or None) | The minimum permitted value. If this is None (default), the minimum value depends on the type as follows:   - integer: 0 - float: 0.0 - date or datetime: value - timedelta(days=14) - time: time.min |
| max\_value (a supported type or None) | The maximum permitted value. If this is None (default), the maximum value depends on the type as follows:   - integer: 100 - float: 1.0 - date or datetime: value + timedelta(days=14) - time: time.max |
| value (a supported type or a tuple/list of supported types or None) | The value of the slider when it first renders. If a tuple/list of two values is passed here, then a range slider with those lower and upper bounds is rendered. For example, if set to (1, 10) the slider will have a selectable range between 1 and 10. This defaults to min\_value. If the type is not otherwise specified in any of the numeric parameters, the widget will have an integer value. |
| step (int, float, timedelta, or None) | The stepping interval. Defaults to 1 if the value is an int, 0.01 if a float, timedelta(days=1) if a date/datetime, timedelta(minutes=15) if a time (or if max\_value - min\_value < 1 day) |
| format (str or None) | A printf-style format string or a predefined format name controlling how the interface should display values. This does not impact the return value.  For integers and floats, you can use a printf-style format string or one of the following predefined formats:   - "plain": Show the full number without formatting (e.g. 1234.567). - "localized": Show the number in the user's locale format (e.g. 1,234.567). - "percent": Show as a percentage (e.g. 50% from 0.5). - "dollar": Show as US dollars (e.g. $1,234.57). - "euro": Show as euros (e.g. €1,234.57). - "yen": Show as Japanese yen (e.g. ¥1,235). - "compact": Show in compact notation (e.g. 1.2K). - "scientific": Show in scientific notation (e.g. 1.235E3). - "engineering": Show in engineering notation (e.g. 1.235E3). - "accounting": Show in accounting format with parentheses for negatives. - "bytes": Show in byte units (e.g. 1.2KB).   For information about printf-style format strings, see [sprintf.js](https://github.com/alexei/sprintf.js?tab=readme-ov-file#format-specification). For example, format="%0.1f" adjusts the displayed decimal precision to only show one digit after the decimal. Use , for thousand separators (e.g. "%,d" yields "1,234").  For datetimes, dates, and times, you can use a momentJS format string or one of the following predefined formats:   - "localized": Show in the user's locale format. - "distance": Show as relative time (e.g. "2 hours ago"). - "calendar": Show as calendar time (e.g. "Tomorrow 12:00").   Works best with datetime values. For date-only values, displays   relative day names (e.g. "Yesterday"). For time-only values,   this format may produce unexpected results. - "iso8601": Show in ISO 8601 format.   For information about momentJS format strings, see [momentJS](https://momentjs.com/docs/#/displaying/format/). For example, format="ddd ha" adjusts the displayed datetime to show the day of the week and the hour ("Tue 8pm"). |
| key (str, int, or None) | An optional string or integer to use as the unique key for the widget. If this is None (default), a key will be generated for the widget based on the values of the other parameters. No two widgets may have the same key. Assigning a key stabilizes the widget's identity and preserves its state across reruns even when other parameters change.  Note  Changing min\_value, max\_value, or step resets the widget even when a key is provided, because those parameters constrain valid values.  A key lets you read or update the widget's value via st.session\_state[key]. For more details, see [Widget behavior](https://docs.streamlit.io/develop/concepts/architecture/widget-behavior).  Additionally, if key is provided, it will be used as a CSS class name prefixed with st-key-. |
| help (str or None) | A tooltip that gets displayed next to the widget label. Streamlit only displays the tooltip when label\_visibility="visible". If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| on\_change (callable) | An optional callback invoked when this slider's value changes. |
| args (list or tuple) | An optional list or tuple of args to pass to the callback. |
| kwargs (dict) | An optional dict of kwargs to pass to the callback. |
| disabled (bool) | An optional boolean that disables the slider if set to True. The default is False. |
| label\_visibility ("visible", "hidden", or "collapsed") | The visibility of the label. The default is "visible". If this is "hidden", Streamlit displays an empty spacer instead of the label, which can help keep the widget aligned with other widgets. If this is "collapsed", Streamlit displays no label or spacer. |
| width ("stretch" or int) | The width of the slider widget. This can be one of the following:   - "stretch" (default): The width of the widget matches the   width of the parent container. - An integer specifying the width in pixels: The widget has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the widget matches the width   of the parent container. |
| bind ("query-params" or None) | Binding mode for syncing the widget's value with a URL query parameter. If this is None (default), the widget's value is not synced to the URL. When this is set to "query-params", changes to the widget update the URL, and the widget can be initialized or updated through a query parameter in the URL. This requires key to be set. The key is used as the query parameter name.  When the widget's value equals its default, the query parameter is removed from the URL to keep it clean. A bound query parameter can't be set or deleted through st.query\_params; it can only be programmatically changed through st.session\_state.  Invalid query parameter values are ignored and removed from the URL. Range sliders use repeated parameters (e.g., ?price=10&price=90). |
|  |  |
| --- | --- |
| Returns | |
| (int/float/date/time/datetime or tuple of int/float/date/time/datetime) | The current value of the slider widget. The return type will match the data type of the value parameter. |

#### Examples

```
import streamlit as st

age = st.slider("How old are you?", 0, 130, 25)
st.write("I'm ", age, "years old")
```

And here's an example of a range slider:

```
import streamlit as st

values = st.slider("Select a range of values", 0.0, 100.0, (25.0, 75.0))
st.write("Values:", values)
```

This is a range time slider:

```
import streamlit as st
from datetime import time

appointment = st.slider(
    "Schedule your appointment:", value=(time(11, 30), time(12, 45))
)
st.write("You're scheduled for:", appointment)
```

Finally, a datetime slider:

```
import streamlit as st
from datetime import datetime

start_time = st.slider(
    "When do you start?",
    value=datetime(2020, 1, 1, 9, 30),
    format="MM/DD/YY - hh:mm",
)
st.write("Start time:", start_time)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-slider.streamlit.app//?utm_medium=oembed&)

Check out our video on how to use one of Streamlit's core functions, the slider!

In the video below, we'll take it a step further and make a double-ended slider.

[*arrow\_back*Previous: st.number\_input](/develop/api-reference/widgets/st.number_input)[*arrow\_forward*Next: st.date\_input](/develop/api-reference/widgets/st.date_input)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI