<!-- Source: https://docs.streamlit.io/develop/api-reference/data/st.column_config/st.column_config.datetimecolumn -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/lib/column_types.py#L1972 "View st.DatetimeColumn source code on GitHub") | |
| --- | --- |
| st.column\_config.DatetimeColumn(label=None, \*, width=None, help=None, disabled=None, required=None, pinned=None, default=None, format=None, min\_value=None, max\_value=None, step=None, timezone=None) | |
| Parameters | |
| label (str or None) | The label shown at the top of the column. If this is None (default), the column name is used. |
| width ("small", "medium", "large", int, or None) | The display width of the column. If this is None (default), the column will be sized to fit the cell contents. Otherwise, this can be one of the following:   - "small": 75px wide - "medium": 200px wide - "large": 400px wide - An integer specifying the width in pixels   If the total width of all columns is less than the width of the dataframe, the remaining space will be distributed evenly among all columns. |
| help (str or None) | A tooltip that gets displayed when hovering over the column label. If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| disabled (bool or None) | Whether editing should be disabled for this column. If this is None (default), Streamlit will enable editing wherever possible.  If a column has mixed types, it may become uneditable regardless of disabled. |
| required (bool or None) | Whether edited cells in the column need to have a value. If this is False (default), the user can submit empty values for this column. If this is True, an edited cell in this column can only be submitted if its value is not None, and a new row will only be submitted after the user fills in this column. |
| pinned (bool or None) | Whether the column is pinned. A pinned column will stay visible on the left side no matter where the user scrolls. If this is None (default), Streamlit will decide: index columns are pinned, and data columns are not pinned. |
| default (datetime.datetime or None) | Specifies the default value in this column when a new row is added by the user. This defaults to None. |
| format (str, "localized", "distance", "calendar", "iso8601", or None) | A format string controlling how datetimes are displayed. This can be one of the following values:   - None (default): Show the datetime in "YYYY-MM-DD HH:mm:ss"   format (e.g. "2025-03-04 20:00:00"). - "localized": Show the datetime in the default locale format (e.g.   "Mar 4, 2025, 12:00:00 PM" in the America/Los\_Angeles timezone). - "distance": Show the datetime in a relative format (e.g.   "a few seconds ago"). - "calendar": Show the datetime in a calendar format (e.g.   "Today at 8:00 PM"). - "iso8601": Show the datetime in ISO 8601 format (e.g.   "2025-03-04T20:00:00.000Z"). - A momentJS format string: Format the datetime with a string, like   "ddd ha" to show "Tue 8pm". For available formats, see   [momentJS](https://momentjs.com/docs/#/displaying/format/).   Formatting from column\_config always takes precedence over formatting from pandas.Styler. The formatting does not impact the return value when used in st.data\_editor. |
| min\_value (datetime.datetime or None) | The minimum datetime that can be entered. If this is None (default), there will be no minimum. |
| max\_value (datetime.datetime or None) | The maximum datetime that can be entered. If this is None (default), there will be no maximum. |
| step (int, float, datetime.timedelta, or None) | The stepping interval in seconds. If this is None (default), the step will be 1 second. |
| timezone (str or None) | The timezone of this column. If this is None (default), the timezone is inferred from the underlying data. |

#### Examples

```
from datetime import datetime
import pandas as pd
import streamlit as st

data_df = pd.DataFrame(
    {
        "appointment": [
            datetime(2024, 2, 5, 12, 30),
            datetime(2023, 11, 10, 18, 0),
            datetime(2024, 3, 11, 20, 10),
            datetime(2023, 9, 12, 3, 0),
        ]
    }
)

st.data_editor(
    data_df,
    column_config={
        "appointment": st.column_config.DatetimeColumn(
            "Appointment",
            min_value=datetime(2023, 6, 1),
            max_value=datetime(2025, 1, 1),
            format="D MMM YYYY, h:mm a",
            step=60,
        ),
    },
    hide_index=True,
)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-datetime-column.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: Multiselect column](/develop/api-reference/data/st.column_config/st.column_config.multiselectcolumn)[*arrow\_forward*Next: Date column](/develop/api-reference/data/st.column_config/st.column_config.datecolumn)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI