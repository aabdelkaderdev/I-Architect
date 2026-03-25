<!-- Source: https://docs.streamlit.io/develop/api-reference/data/st.column_config/st.column_config.jsoncolumn -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/lib/column_types.py#L2613 "View st.JsonColumn source code on GitHub") | |
| --- | --- |
| st.column\_config.JsonColumn(label=None, \*, width=None, help=None, pinned=None) | |
| Parameters | |
| label (str or None) | The label shown at the top of the column. If this is None (default), the column name is used. |
| width ("small", "medium", "large", int, or None) | The display width of the column. If this is None (default), the column will be sized to fit the cell contents. Otherwise, this can be one of the following:   - "small": 75px wide - "medium": 200px wide - "large": 400px wide - An integer specifying the width in pixels   If the total width of all columns is less than the width of the dataframe, the remaining space will be distributed evenly among all columns. |
| help (str or None) | A tooltip that gets displayed when hovering over the column label. If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| pinned (bool or None) | Whether the column is pinned. A pinned column will stay visible on the left side no matter where the user scrolls. If this is None (default), Streamlit will decide: index columns are pinned, and data columns are not pinned. |

#### Examples

```
import pandas as pd
import streamlit as st

data_df = pd.DataFrame(
    {
        "json": [
            {"foo": "bar", "bar": "baz"},
            {"foo": "baz", "bar": "qux"},
            {"foo": "qux", "bar": "foo"},
            None,
        ],
    }
)

st.dataframe(
    data_df,
    column_config={
        "json": st.column_config.JsonColumn(
            "JSON Data",
            help="JSON strings or objects",
            width="large",
        ),
    },
    hide_index=True,
)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-json-column.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: Time column](/develop/api-reference/data/st.column_config/st.column_config.timecolumn)[*arrow\_forward*Next: List column](/develop/api-reference/data/st.column_config/st.column_config.listcolumn)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI