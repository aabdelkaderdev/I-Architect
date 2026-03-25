<!-- Source: https://docs.streamlit.io/develop/api-reference/data/st.table -->

Show API reference for

Version v1.55.0*expand\_more*

Static tables with `st.table` are the most basic way to display dataframes. For the majority of cases, we recommend using [`st.dataframe`](/develop/api-reference/data/st.dataframe) to display interactive dataframes, and [`st.data_editor`](/develop/api-reference/data/st.data_editor) to let users edit dataframes.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/table.py#L82 "View st.table source code on GitHub") | |
| --- | --- |
| st.table(data=None, \*, border=True, width="stretch", height="content") | |
| Parameters | |
| data (Anything supported by st.dataframe) | The table data.  All cells including the index and column headers can optionally contain GitHub-flavored Markdown. Syntax information can be found at: <https://github.github.com/gfm>.  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives. |
| border (bool or "horizontal") | Whether to show borders around the table and between cells. This can be one of the following:   - True (default): Show borders around the table and between cells. - False: Don't show any borders. - "horizontal": Show only horizontal borders between rows. |
| width ("stretch", "content", or int) | The width of the table element. This can be one of the following:   - "stretch" (default): The width of the element matches the   width of the parent container. - "content": The width of the element matches the width of its   content, but doesn't exceed the width of the parent container. - An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container.   Row index columns are sticky only when the content overflows a specified integer width. Otherwise, they aren't sticky. |
| height ("stretch", "content", or int) | The height of the table element. This can be one of the following:   - "content" (default): The height of the element matches the   height of its content, showing all rows. - "stretch": The height of the element expands to fill the   available vertical space in its parent container. When multiple   elements with stretch height are in the same container, they   share the available vertical space evenly. - An integer specifying the height in pixels: The element has a   fixed height. If the table content exceeds this height,   scrolling is enabled with sticky headers. |

#### Examples

**Example 1: Display a confusion matrix as a static table**

```
import pandas as pd
import streamlit as st

confusion_matrix = pd.DataFrame(
    {
        "Predicted Cat": [85, 3, 2, 1],
        "Predicted Dog": [2, 78, 4, 0],
        "Predicted Bird": [1, 5, 72, 3],
        "Predicted Fish": [0, 2, 1, 89],
    },
    index=["Actual Cat", "Actual Dog", "Actual Bird", "Actual Fish"],
)
st.table(confusion_matrix)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-table-confusion.streamlit.app//?utm_medium=oembed&)

**Example 2: Display a product leaderboard with Markdown and horizontal borders**

```
import streamlit as st

product_data = {
    "Product": [
        ":material/devices: Widget Pro",
        ":material/smart_toy: Smart Device",
        ":material/inventory: Premium Kit",
    ],
    "Category": [":blue[Electronics]", ":green[IoT]", ":violet[Bundle]"],
    "Stock": ["🟢 Full", "🟡 Low", "🔴 Empty"],
    "Units sold": [1247, 892, 654],
    "Revenue": [125000, 89000, 98000],
}
st.table(product_data, border="horizontal")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-table-horizontal-border.streamlit.app//?utm_medium=oembed&)

**Example 3: Display a scrollable table with fixed height**

```
import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng

df = pd.DataFrame(
    rng(0).standard_normal((50, 5)), columns=["A", "B", "C", "D", "E"]
)
st.table(df, height=300)
```

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/arrow.py#L809 "View st.add_rows source code on GitHub") | |
| --- | --- |
| element.add\_rows(data=None, \*\*kwargs) | |
| Parameters | |
| data (pandas.DataFrame, pandas.Styler, pyarrow.Table, numpy.ndarray, pyspark.sql.DataFrame, snowflake.snowpark.dataframe.DataFrame, Iterable, dict, or None) | Table to concat. Optional. |
| \*\*kwargs (pandas.DataFrame, numpy.ndarray, Iterable, dict, or None) | The named dataset to concat. Optional. You can only pass in 1 dataset (including the one in the data parameter). |

#### Example

```
import time
import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng

df1 = pd.DataFrame(
    rng(0).standard_normal(size=(50, 20)), columns=("col %d" % i for i in range(20))
)

df2 = pd.DataFrame(
    rng(1).standard_normal(size=(50, 20)), columns=("col %d" % i for i in range(20))
)

my_table = st.table(df1)
time.sleep(1)
my_table.add_rows(df2)
```

You can do the same thing with plots. For example, if you want to add
more data to a line chart:

```
# Assuming df1 and df2 from the example above still exist...
my_chart = st.line_chart(df1)
time.sleep(1)
my_chart.add_rows(df2)
```

And for plots whose datasets are named, you can pass the data with a
keyword argument where the key is the name:

```
my_chart = st.vega_lite_chart(
    {
        "mark": "line",
        "encoding": {"x": "a", "y": "b"},
        "datasets": {
            "some_fancy_name": df1,  # <-- named dataset
        },
        "data": {"name": "some_fancy_name"},
    }
)
my_chart.add_rows(some_fancy_name=df2)  # <-- name used as keyword
```

[*arrow\_back*Previous: st.column\_config](/develop/api-reference/data/st.column_config)[*arrow\_forward*Next: st.metric](/develop/api-reference/data/st.metric)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI