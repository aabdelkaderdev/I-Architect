<!-- Source: https://docs.streamlit.io/develop/api-reference/charts/st.pydeck_chart -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/deck_gl_json_chart.py#L300 "View st.pydeck_chart source code on GitHub") | |
| --- | --- |
| st.pydeck\_chart(pydeck\_obj=None, \*, width="stretch", use\_container\_width=None, height=500, selection\_mode="single-object", on\_select="ignore", key=None) | |
| Parameters | |
| pydeck\_obj (pydeck.Deck or None) | Object specifying the PyDeck chart to draw. |
| width ("stretch" or int) | The width of the chart element. This can be one of the following:   - "stretch" (default): The width of the element matches the   width of the parent container. - An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container. |
| use\_container\_width (bool or None) | *delete* use\_container\_width is deprecated and will be removed in a future release. For use\_container\_width=True, use width="stretch".  Whether to override the chart's native width with the width of the parent container. This can be one of the following:   - None (default): Streamlit will use the chart's default behavior. - True: Streamlit sets the width of the chart to match the   width of the parent container. - False: Streamlit sets the width of the chart to fit its   contents according to the plotting library, up to the width of   the parent container. |
| height ("stretch" or int) | The height of the chart element. This can be one of the following:   - An integer specifying the height in pixels: The element has a   fixed height. If the content is larger than the specified   height, scrolling is enabled. This is 500 by default. - "stretch": The height of the element matches the height of   its content or the height of the parent container, whichever is   larger. If the element is not in a parent container, the height   of the element matches the height of its content. |
| on\_select ("ignore" or "rerun" or callable) | How the figure should respond to user selection events. This controls whether or not the chart behaves like an input widget. on\_select can be one of the following:   - "ignore" (default): Streamlit will not react to any selection   events in the chart. The figure will not behave like an   input widget. - "rerun": Streamlit will rerun the app when the user selects   data in the chart. In this case, st.pydeck\_chart will return   the selection data as a dictionary. - A callable: Streamlit will rerun the app and execute the callable   as a callback function before the rest of the app. In this case,   st.pydeck\_chart will return the selection data as a   dictionary.   If on\_select is not "ignore", all layers must have a declared id to keep the chart stateful across reruns. |
| selection\_mode ("single-object" or "multi-object") | The selection mode of the chart. This can be one of the following:   - "single-object" (default): Only one object can be selected at   a time. - "multi-object": Multiple objects can be selected at a time. |
| key (str, int, or None) | An optional string to use for giving this element a stable identity. If this is None (default), the element's identity will be determined based on the values of the other parameters.  If selections are activated and key is provided, Streamlit will register the key in Session State to store the selection state. The selection state is read-only. For more details, see [Widget behavior](https://docs.streamlit.io/develop/concepts/architecture/widget-behavior).  Additionally, if key is provided, it will be used as a CSS class name prefixed with st-key-. |
|  |  |
| --- | --- |
| Returns | |
| (element or dict) | If on\_select is "ignore" (default), this command returns an internal placeholder for the chart element. Otherwise, this method returns a dictionary-like object that supports both key and attribute notation. The attributes are described by the PydeckState dictionary schema. |

#### Example

Here's a chart using a HexagonLayer and a ScatterplotLayer. It uses either the
light or dark map style, based on which Streamlit theme is currently active:

```
import pandas as pd
import pydeck as pdk
import streamlit as st
from numpy.random import default_rng as rng

df = pd.DataFrame(
    rng(0).standard_normal((1000, 2)) / [50, 50] + [37.76, -122.4],
    columns=["lat", "lon"],
)

st.pydeck_chart(
    pdk.Deck(
        map_style=None,  # Use Streamlit theme to pick map style
        initial_view_state=pdk.ViewState(
            latitude=37.76,
            longitude=-122.4,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=df,
                get_position="[lon, lat]",
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position="[lon, lat]",
                get_color="[200, 30, 0, 160]",
                get_radius=200,
            ),
        ],
    )
)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-pydeck-chart.streamlit.app//?utm_medium=oembed&)

Note

To make the PyDeck chart's style consistent with Streamlit's theme,
you can set map\_style=None in the pydeck.Deck object.

|  |  |
| --- | --- |
| Attributes | |
| selection (dict) | The state of the on\_select event. This attribute returns a dictionary-like object that supports both key and attribute notation. The attributes are described by the PydeckSelectionState dictionary schema. |

|  |  |
| --- | --- |
| Attributes | |
| indices (dict[str, list[int]]) | A dictionary of selected objects by layer. Each key in the dictionary is a layer id, and each value is a list of object indices within that layer. |
| objects (dict[str, list[dict[str, Any]]]) | A dictionary of object attributes by layer. Each key in the dictionary is a layer id, and each value is a list of metadata dictionaries for the selected objects in that layer. |

#### Examples

The following example has multi-object selection enabled. The chart
displays US state capitals by population (2023 US Census estimate). You
can access this [data](https://github.com/streamlit/docs/blob/main/python/api-examples-source/data/capitals.csv)
from GitHub.

```
import streamlit as st
import pydeck
import pandas as pd

capitals = pd.read_csv(
    "capitals.csv",
    header=0,
    names=[
        "Capital",
        "State",
        "Abbreviation",
        "Latitude",
        "Longitude",
        "Population",
    ],
)
capitals["size"] = capitals.Population / 10

point_layer = pydeck.Layer(
    "ScatterplotLayer",
    data=capitals,
    id="capital-cities",
    get_position=["Longitude", "Latitude"],
    get_color="[255, 75, 75]",
    pickable=True,
    auto_highlight=True,
    get_radius="size",
)

view_state = pydeck.ViewState(
    latitude=40, longitude=-117, controller=True, zoom=2.4, pitch=30
)

chart = pydeck.Deck(
    point_layer,
    initial_view_state=view_state,
    tooltip={"text": "{Capital}, {Abbreviation}\nPopulation: {Population}"},
)

event = st.pydeck_chart(chart, on_select="rerun", selection_mode="multi-object")

event.selection
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-pydeck-event-state-selections.streamlit.app//?utm_medium=oembed&)

This is an example of the selection state when selecting a single object
from a layer with id, "captial-cities":

```
{
  "indices":{
    "capital-cities":[
      2
    ]
  },
  "objects":{
    "capital-cities":[
      {
        "Abbreviation":" AZ"
        "Capital":"Phoenix"
        "Latitude":33.448457
        "Longitude":-112.073844
        "Population":1650070
        "State":" Arizona"
        "size":165007.0
      }
    ]
  }
}
```

[*arrow\_back*Previous: st.plotly\_chart](/develop/api-reference/charts/st.plotly_chart)[*arrow\_forward*Next: st.pyplot](/develop/api-reference/charts/st.pyplot)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI