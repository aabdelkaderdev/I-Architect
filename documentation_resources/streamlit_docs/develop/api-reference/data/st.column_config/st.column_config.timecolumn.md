<!-- Source: https://docs.streamlit.io/develop/api-reference/data/st.column_config/st.column_config.timecolumn -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/lib/column_types.py#L2140 "View st.TimeColumn source code on GitHub") | |
| --- | --- |
| st.column\_config.TimeColumn(label=None, \*, width=None, help=None, disabled=None, required=None, pinned=None, default=None, format=None, min\_value=None, max\_value=None, step=None) | |
| Parameters | |
| label (str or None) | The label shown at the top of the column. If this is None (default), the column name is used. |
| width ("small", "medium", "large", int, or None) | The display width of the column. If this is None (default), the column will be sized to fit the cell contents. Otherwise, this can be one of the following:   - "small": 75px wide - "medium": 200px wide - "large": 400px wide - An integer specifying the width in pixels   If the total width of all columns is less than the width of the dataframe, the remaining space will be distributed evenly among all columns. |
| help (str or None) | A tooltip that gets displayed when hovering over the column label. If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| disabled (bool or None) | Whether editing should be disabled for this column. If this is None (default), Streamlit will enable editing wherever possible.  If a column has mixed types, it may become uneditable regardless of disabled. |
| required (bool or None) | Whether edited cells in the column need to have a value. If this is False (default), the user can submit empty values for this column. If this is True, an edited cell in this column can only be submitted if its value is not None, and a new row will only be submitted after the user fills in this column. |
| pinned (bool or None) | Whether the column is pinned. A pinned column will stay visible on the left side no matter where the user scrolls. If this is None (default), Streamlit will decide: index columns are pinned, and data columns are not pinned. |
| default (datetime.time or None) | Specifies the default value in this column when a new row is added by the user. This defaults to None. |
| format (str, "localized", "iso8601", or None) | A format string controlling how times are displayed. This can be one of the following values:   - None (default): Show the time in "HH:mm:ss" format (e.g.   "20:00:00"). - "localized": Show the time in the default locale format (e.g.   "12:00:00 PM" in the America/Los\_Angeles timezone). - "iso8601": Show the time in ISO 8601 format (e.g.   "20:00:00.000Z"). - A momentJS format string: Format the time with a string, like   "ha" to show "8pm". For available formats, see   [momentJS](https://momentjs.com/docs/#/displaying/format/).   Formatting from column\_config always takes precedence over formatting from pandas.Styler. The formatting does not impact the return value when used in st.data\_editor. |
| min\_value (datetime.time or None) | The minimum time that can be entered. If this is None (default), there will be no minimum. |
| max\_value (datetime.time or None) | The maximum time that can be entered. If this is None (default), there will be no maximum. |
| step (int, float, datetime.timedelta, or None) | The stepping interval in seconds. If this is None (default), the step will be 1 second. |

#### Examples

```
from datetime import time
import pandas as pd
import streamlit as st

data_df = pd.DataFrame(
    {
        "appointment": [
            time(12, 30),
            time(18, 0),
            time(9, 10),
            time(16, 25),
        ]
    }
)

st.data_editor(
    data_df,
    column_config={
        "appointment": st.column_config.TimeColumn(
            "Appointment",
            min_value=time(8, 0, 0),
            max_value=time(19, 0, 0),
            format="hh:mm a",
            step=60,
        ),
    },
    hide_index=True,
)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-time-column.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: Date column](/develop/api-reference/data/st.column_config/st.column_config.datecolumn)[*arrow\_forward*Next: JSON column](/develop/api-reference/data/st.column_config/st.column_config.jsoncolumn)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI