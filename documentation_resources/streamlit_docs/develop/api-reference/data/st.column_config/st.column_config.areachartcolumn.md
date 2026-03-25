<!-- Source: https://docs.streamlit.io/develop/api-reference/data/st.column_config/st.column_config.areachartcolumn -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/lib/column_types.py#L1395 "View st.AreaChartColumn source code on GitHub") | |
| --- | --- |
| st.column\_config.AreaChartColumn(label=None, \*, width=None, help=None, pinned=None, y\_min=None, y\_max=None, color=None) | |
| Parameters | |
| label (str or None) | The label shown at the top of the column. If this is None (default), the column name is used. |
| width ("small", "medium", "large", int, or None) | The display width of the column. If this is None (default), the column will be sized to fit the cell contents. Otherwise, this can be one of the following:   - "small": 75px wide - "medium": 200px wide - "large": 400px wide - An integer specifying the width in pixels   If the total width of all columns is less than the width of the dataframe, the remaining space will be distributed evenly among all columns. |
| help (str or None) | A tooltip that gets displayed when hovering over the column label. If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| pinned (bool or None) | Whether the column is pinned. A pinned column will stay visible on the left side no matter where the user scrolls. If this is None (default), Streamlit will decide: index columns are pinned, and data columns are not pinned. |
| y\_min (int, float, or None) | The minimum value on the y-axis for all cells in the column. If this is None (default), every cell will use the minimum of its data. |
| y\_max (int, float, or None) | The maximum value on the y-axis for all cells in the column. If this is None (default), every cell will use the maximum of its data. |
| color ("auto", "auto-inverse", str, or None) | The color to use for the chart. This can be one of the following:   - None (default): The primary color is used. - "auto": If the data is increasing, the chart is green; if the   data is decreasing, the chart is red. - "auto-inverse": If the data is increasing, the chart is red; if   the data is decreasing, the chart is green. - A single color value that is applied to all charts in the column.   In addition to the basic color palette (red, orange, yellow, green,   blue, violet, gray/grey, and primary), this supports hex codes like   "#483d8b".   The basic color palette can be configured in the theme settings. |

#### Examples

```
import pandas as pd
import streamlit as st

data_df = pd.DataFrame(
    {
        "sales": [
            [0, 4, 26, 80, 100, 40],
            [80, 20, 80, 35, 40, 100],
            [10, 20, 80, 80, 70, 0],
            [10, 100, 20, 100, 30, 100],
        ],
    }
)

st.data_editor(
    data_df,
    column_config={
        "sales": st.column_config.AreaChartColumn(
            "Sales (last 6 months)",
            width="medium",
            help="The sales volume in the last 6 months",
            y_min=0,
            y_max=100,
         ),
    },
    hide_index=True,
)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-areachart-column.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: Image column](/develop/api-reference/data/st.column_config/st.column_config.imagecolumn)[*arrow\_forward*Next: Line chart column](/develop/api-reference/data/st.column_config/st.column_config.linechartcolumn)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI