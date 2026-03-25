<!-- Source: https://docs.streamlit.io/develop/api-reference/charts/st.scatter_chart -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/vega_charts.py#L1541 "View st.scatter_chart source code on GitHub") | |
| --- | --- |
| st.scatter\_chart(data=None, \*, x=None, y=None, x\_label=None, y\_label=None, color=None, size=None, width="stretch", height="content", use\_container\_width=None) | |
| Parameters | |
| data (Anything supported by st.dataframe) | Data to be plotted. |
| x (str or None) | Column name or key associated to the x-axis data. If x is None (default), Streamlit uses the data index for the x-axis values. |
| y (str, Sequence of str, or None) | Column name(s) or key(s) associated to the y-axis data. If this is None (default), Streamlit draws the data of all remaining columns as data series. If this is a Sequence of strings, Streamlit draws several series on the same chart by melting your wide-format table into a long-format table behind the scenes. |
| x\_label (str or None) | The label for the x-axis. If this is None (default), Streamlit will use the column name specified in x if available, or else no label will be displayed. |
| y\_label (str or None) | The label for the y-axis. If this is None (default), Streamlit will use the column name(s) specified in y if available, or else no label will be displayed. |
| color (str, tuple, Sequence of str, Sequence of tuple, or None) | The color of the circles representing each datapoint.  This can be:   - None, to use the default color. - A hex string like "#ffaa00" or "#ffaa0088". - An RGB or RGBA tuple with the red, green, blue, and alpha   components specified as ints from 0 to 255 or floats from 0.0 to   1.0. - A built-in color name: "red", "orange", "yellow", "green",   "blue", "violet", "gray"/"grey", or "primary". These map to   theme colors that you can customize using theme.<color>Color   configuration options. - The name of a column in the dataset where the color of that   datapoint will come from.  If the values in this column are in one of the color formats   above (hex string or color tuple), then that color will be used.  Otherwise, the color will be automatically picked from the   default palette.  For example: if the dataset has 1000 rows, but this column only   contains the values "adult", "child", and "baby", then those 1000   datapoints be shown using three colors from the default palette.  But if this column only contains floats or ints, then those   1000 datapoints will be shown using a colors from a continuous   color gradient.  Finally, if this column only contains the values "#ffaa00",   "#f0f", "#0000ff", then then each of those 1000 datapoints will   be assigned "#ffaa00", "#f0f", or "#0000ff" as appropriate.   If the dataframe is in wide format (that is, y is a Sequence of columns), this can also be:   - A list of string colors or color tuples to be used for each of   the series in the chart. This list should have the same length   as the number of y values (e.g. color=["#fd0", "#f0f", "#04f"]   for three series). You can also use built-in color names in the   list (e.g. color=["red", "blue", "green"]). |
| size (str, float, int, or None) | The size of the circles representing each point.  This can be:   - A number like 100, to specify a single size to use for all   datapoints. - The name of the column to use for the size. This allows each   datapoint to be represented by a circle of a different size. |
| width ("stretch", "content", or int) | The width of the chart element. This can be one of the following:   - "stretch" (default): The width of the element matches the   width of the parent container. - "content": The width of the element matches the width of its   content, but doesn't exceed the width of the parent container. - An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container. |
| height ("stretch", "content", or int) | The height of the chart element. This can be one of the following:   - "content" (default): The height of the element matches the   height of its content. - "stretch": The height of the element matches the height of   its content or the height of the parent container, whichever is   larger. If the element is not in a parent container, the height   of the element matches the height of its content. - An integer specifying the height in pixels: The element has a   fixed height. If the content is larger than the specified   height, scrolling is enabled. |
| use\_container\_width (bool or None) | *delete* use\_container\_width is deprecated and will be removed in a future release. For use\_container\_width=True, use width="stretch".  Whether to override the chart's native width with the width of the parent container. This can be one of the following:   - None (default): Streamlit will use the chart's default behavior. - True: Streamlit sets the width of the chart to match the   width of the parent container. - False: Streamlit sets the width of the chart to fit its   contents according to the plotting library, up to the width of   the parent container. |

#### Examples

**Example 1: Basic scatter chart from a dataframe**

If you don't use any of the optional parameters, Streamlit plots each
column as a color-coded group of points, uses the index as the x
values, and labels each group with the column name:

```
import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng

df = pd.DataFrame(rng(0).standard_normal((20, 3)), columns=["a", "b", "c"])

st.scatter_chart(df)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-scatter-chart.streamlit.app//?utm_medium=oembed&)

**Example 2: Scatter chart from specific dataframe columns**

You can choose different columns to use for the x and y values. If your
dataframe is in long format (all y-values in one column), you can set
the scatter point colors from another column.

If the column contains color strings, the colors will be applied
directly and each color group will be unlabeled. If the column contains
other values, those values will label each group, and the scatter point
colors will be selected from the default color palette. You can
configure this color palette in the theme.chartCategoryColors
configuration option.

```
import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng

df = pd.DataFrame(
    rng(0).standard_normal((20, 3)), columns=["col1", "col2", "col3"]
)
df["col4"] = rng(0).choice(["a", "b", "c"], 20)

st.scatter_chart(
    df,
    x="col1",
    y="col2",
    color="col4",
    size="col3",
)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-scatter-chart1.streamlit.app//?utm_medium=oembed&)

**Example 3: Scatter chart from wide-format dataframe**

If your dataframe is in wide format (y-values are in multiple columns),
you can pass a list of columns to the y parameter. Each column
name becomes a group label. To override the default colors, pass a
list of colors to the color parameter, one for each group:

```
import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng

df = pd.DataFrame(
    rng(0).standard_normal((20, 4)),
    columns=["col1", "col2", "col3", "col4"],
)

st.scatter_chart(
    df,
    x="col1",
    y=["col2", "col3"],
    size="col4",
    color=["#FF0000", "#0000FF"],
)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-scatter-chart2.streamlit.app//?utm_medium=oembed&)

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

[*arrow\_back*Previous: st.map](/develop/api-reference/charts/st.map)[*arrow\_forward*Next: st.altair\_chart](/develop/api-reference/charts/st.altair_chart)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI