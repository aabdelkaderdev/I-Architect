<!-- Source: https://docs.streamlit.io/develop/api-reference/charts/st.map -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/map.py#L89 "View st.map source code on GitHub") | |
| --- | --- |
| st.map(data=None, \*, latitude=None, longitude=None, color=None, size=None, zoom=None, width="stretch", height=500, use\_container\_width=None) | |
| Parameters | |
| data (Anything supported by st.dataframe) | The data to be plotted. |
| latitude (str or None) | The name of the column containing the latitude coordinates of the datapoints in the chart.  If None, the latitude data will come from any column named 'lat', 'latitude', 'LAT', or 'LATITUDE'. |
| longitude (str or None) | The name of the column containing the longitude coordinates of the datapoints in the chart.  If None, the longitude data will come from any column named 'lon', 'longitude', 'LON', or 'LONGITUDE'. |
| color (str or tuple or None) | The color of the circles representing each datapoint.  Can be:   - None, to use the default color. - A hex string like "#ffaa00" or "#ffaa0088". - An RGB or RGBA tuple with the red, green, blue, and alpha   components specified as ints from 0 to 255 or floats from 0.0 to   1.0. - The name of the column to use for the color. Cells in this column   should contain colors represented as a hex string or color tuple,   as described above. |
| size (str or float or None) | The size of the circles representing each point, in meters.  This can be:   - None, to use the default size. - A number like 100, to specify a single size to use for all   datapoints. - The name of the column to use for the size. This allows each   datapoint to be represented by a circle of a different size. |
| zoom (int) | Zoom level as specified in <https://wiki.openstreetmap.org/wiki/Zoom_levels>. |
| width ("stretch" or int) | The width of the chart element. This can be one of the following:   - "stretch" (default): The width of the element matches the   width of the parent container. - An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container. |
| height ("stretch" or int) | The height of the chart element. This can be one of the following:   - An integer specifying the height in pixels: The element has a   fixed height. If the content is larger than the specified   height, scrolling is enabled. This is 500 by default. - "stretch": The height of the element matches the height of   its content or the height of the parent container, whichever is   larger. If the element is not in a parent container, the height   of the element matches the height of its content. |
| use\_container\_width (bool or None) | *delete* use\_container\_width is deprecated and will be removed in a future release. For use\_container\_width=True, use width="stretch".  Whether to override the map's native width with the width of the parent container. This can be one of the following:   - None (default): Streamlit will use the map's default behavior. - True: Streamlit sets the width of the map to match the   width of the parent container. - False: Streamlit sets the width of the map to fit its   contents according to the plotting library, up to the width of   the parent container. |

#### Examples

```
import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng

df = pd.DataFrame(
    rng(0).standard_normal((1000, 2)) / [50, 50] + [37.76, -122.4],
    columns=["lat", "lon"],
)

st.map(df)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-map.streamlit.app//?utm_medium=oembed&)

You can also customize the size and color of the datapoints:

```
st.map(df, size=20, color="#0044ff")
```

And finally, you can choose different columns to use for the latitude
and longitude components, as well as set size and color of each
datapoint dynamically based on other columns:

```
import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng

df = pd.DataFrame(
    {
        "col1": rng(0).standard_normal(1000) / 50 + 37.76,
        "col2": rng(1).standard_normal(1000) / 50 + -122.4,
        "col3": rng(2).standard_normal(1000) * 100,
        "col4": rng(3).standard_normal((1000, 4)).tolist(),
    }
)

st.map(df, latitude="col1", longitude="col2", size="col3", color="col4")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-map-color.streamlit.app//?utm_medium=oembed&)

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

[*arrow\_back*Previous: st.line\_chart](/develop/api-reference/charts/st.line_chart)[*arrow\_forward*Next: st.scatter\_chart](/develop/api-reference/charts/st.scatter_chart)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI