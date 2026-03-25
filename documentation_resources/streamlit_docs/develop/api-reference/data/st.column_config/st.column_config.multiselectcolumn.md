<!-- Source: https://docs.streamlit.io/develop/api-reference/data/st.column_config/st.column_config.multiselectcolumn -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/lib/column_types.py#L1731 "View st.MultiselectColumn source code on GitHub") | |
| --- | --- |
| st.column\_config.MultiselectColumn(label=None, \*, width=None, help=None, disabled=None, required=None, pinned=None, default=None, options=None, accept\_new\_options=None, color=None, format\_func=None) | |
| Parameters | |
| label (str or None) | The label shown at the top of the column. If None (default), the column name is used. |
| width ("small", "medium", "large", or None) | The display width of the column. If this is None (default), the column will be sized to fit the cell contents. Otherwise, this can be one of the following:   - "small": 75px wide - "medium": 200px wide - "large": 400px wide - An integer specifying the width in pixels   If the total width of all columns is less than the width of the dataframe, the remaining space will be distributed evenly among all columns. |
| help (str or None) | A tooltip that gets displayed when hovering over the column label. If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| disabled (bool or None) | Whether editing should be disabled for this column. Defaults to False. |
| required (bool or None) | Whether edited cells in the column need to have a value. If True, an edited cell can only be submitted if it has a value other than None. Defaults to False. |
| pinned (bool or None) | Whether the column is pinned. A pinned column will stay visible on the left side no matter where the user scrolls. If this is None (default), Streamlit will decide: index columns are pinned, and data columns are not pinned. |
| default (Iterable of str or None) | Specifies the default value in this column when a new row is added by the user. |
| options (Iterable of str or None) | The options that can be selected during editing. |
| accept\_new\_options (bool or None) | Whether the user can add selections that aren't included in options. If this is False (default), the user can only select from the items in options. If this is True, the user can enter new items that don't exist in options.  When a user enters and selects a new item, it is included in the returned cell list value as a string. The new item is not added to the options drop-down menu. |
| color (str, Iterable of str, or None) | The color to use for different options. This can be:   - None (default): The options are displayed without color. - "auto": The options are colored based on the configured categorical chart colors. - A single color value that is used for all options. This can be one of   the following strings:  - "primary" to use the primary theme color.   - A CSS named color name like "darkBlue" or "maroon".   - A hex color code like "#483d8b" or "#6A5ACD80".   - An RGB or RGBA color code like "rgb(255,0,0)" or     "RGB(70, 130, 180, .7)".   - An HSL or HSLA color code like "hsl(248, 53%, 58%)"     or "HSL(147, 50%, 47%, .3)". - An iterable of color values that are mapped to the options. The colors   are applied in sequence, cycling through the iterable if there are   more options than colors. |
| format\_func (function or None) | Function to modify the display of the options. It receives the raw option defined in options as an argument and should output the label to be shown for that option. When used in st.data\_editor, this has no impact on the returned value. If this is None (default), the raw option is used as the label. |

#### Examples

**Example 1: Editable multiselect column**

To customize the label colors, provide a list of colors to the color
parameter. You can also format the option labels with the format\_func
parameter.

```
import pandas as pd
import streamlit as st

data_df = pd.DataFrame(
    {
        "category": [
            ["exploration", "visualization"],
            ["llm", "visualization"],
            ["exploration"],
        ],
    }
)

st.data_editor(
    data_df,
    column_config={
        "category": st.column_config.MultiselectColumn(
            "App Categories",
            help="The categories of the app",
            options=[
                "exploration",
                "visualization",
                "llm",
            ],
            color=["#ffa421", "#803df5", "#00c0f2"],
            format_func=lambda x: x.capitalize(),
        ),
    },
)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-multiselect-column-1.streamlit.app//?utm_medium=oembed&)

**Example 2: Colored tags for st.dataframe**

When using st.dataframe, the multiselect column is read-only
and can be used to display colored tags. In this example, the dataframe
uses the primary theme color for all tags.

```
import pandas as pd
import streamlit as st

data_df = pd.DataFrame(
    {
        "category": [
            ["exploration", "visualization"],
            ["llm", "visualization"],
            ["exploration"],
        ],
    }
)

st.dataframe(
    data_df,
    column_config={
        "category": st.column_config.MultiselectColumn(
            "App Categories",
            options=["exploration", "visualization", "llm"],
            color="primary",
            format_func=lambda x: x.capitalize(),
        ),
    },
)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-multiselect-column-2.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: Selectbox column](/develop/api-reference/data/st.column_config/st.column_config.selectboxcolumn)[*arrow\_forward*Next: Datetime column](/develop/api-reference/data/st.column_config/st.column_config.datetimecolumn)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI