<!-- Source: https://docs.streamlit.io/develop/api-reference/data -->

When you're working with data, it is extremely valuable to visualize that
data quickly, interactively, and from multiple different angles. That's what
Streamlit is actually built and optimized for.

You can display data via [charts](/develop/api-reference/data#display-charts), and you can display it in
raw form. These are the Streamlit commands you can use to display and interact with raw data.

[#### Dataframes

Display a dataframe as an interactive table.

```
st.dataframe(my_data_frame)
```](/develop/api-reference/data/st.dataframe)[#### Data editor

Display a data editor widget.

```
edited = st.data_editor(df, num_rows="dynamic")
```](/develop/api-reference/data/st.data_editor)[#### Column configuration

Configure the display and editing behavior of dataframes and data editors.

```
st.column_config.NumberColumn("Price (in USD)", min_value=0, format="$%d")
```](/develop/api-reference/data/st.column_config)[#### Static tables

Display a static table.

```
st.table(my_data_frame)
```](/develop/api-reference/data/st.table)[#### Metrics

Display a metric in big bold font, with an optional indicator of how the metric changed.

```
st.metric("My metric", 42, 2)
```](/develop/api-reference/data/st.metric)[#### Dicts and JSON

Display object or string as a pretty-printed JSON string.

```
st.json(my_dict)
```](/develop/api-reference/data/st.json)

Third-party components

These are featured components created by our lovely community. For more examples and inspiration, check out our [Components Gallery](https://streamlit.io/components) and [Streamlit Extras](https://extras.streamlit.app)!

Previous

#### Image Coordinates

Get the coordinates of clicks on an image. Created by [@blackary](https://github.com/blackary/).

```
from streamlit_image_coordinates import streamlit_image_coordinates
value = streamlit_image_coordinates("https://placekitten.com/200/300")

st.write(value)
```

#### Plotly Events

Make Plotly charts interactive!. Created by [@null-jones](https://github.com/null-jones/).

```
from streamlit_plotly_events import plotly_events
fig = px.line(x=[1], y=[1])

selected_points = plotly_events(fig)
```

#### Streamlit Extras

A library with useful Streamlit extras. Created by [@arnaudmiribel](https://github.com/arnaudmiribel/).

```
from streamlit_extras.metric_cards import style_metric_cards
col3.metric(label="No Change", value=5000, delta=0)

style_metric_cards()
```

#### Streamlit Aggrid

Implementation of Ag-Grid component for Streamlit. Created by [@PablocFonseca](https://github.com/PablocFonseca).

```
df = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
grid_return = AgGrid(df, editable=True)

new_df = grid_return['data']
```

#### Streamlit Folium

Streamlit Component for rendering Folium maps. Created by [@randyzwitch](https://github.com/randyzwitch).

```
m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
folium.Marker([39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell").add_to(m)

st_data = st_folium(m, width=725)
```

#### Pandas Profiling

Pandas profiling component for Streamlit. Created by [@okld](https://github.com/okld/).

```
df = pd.read_csv("https://storage.googleapis.com/tf-datasets/titanic/train.csv")
pr = df.profile_report()

st_profile_report(pr)
```

#### Image Coordinates

Get the coordinates of clicks on an image. Created by [@blackary](https://github.com/blackary/).

```
from streamlit_image_coordinates import streamlit_image_coordinates
value = streamlit_image_coordinates("https://placekitten.com/200/300")

st.write(value)
```

#### Plotly Events

Make Plotly charts interactive!. Created by [@null-jones](https://github.com/null-jones/).

```
from streamlit_plotly_events import plotly_events
fig = px.line(x=[1], y=[1])

selected_points = plotly_events(fig)
```

#### Streamlit Extras

A library with useful Streamlit extras. Created by [@arnaudmiribel](https://github.com/arnaudmiribel/).

```
from streamlit_extras.metric_cards import style_metric_cards
col3.metric(label="No Change", value=5000, delta=0)

style_metric_cards()
```

#### Streamlit Aggrid

Implementation of Ag-Grid component for Streamlit. Created by [@PablocFonseca](https://github.com/PablocFonseca).

```
df = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
grid_return = AgGrid(df, editable=True)

new_df = grid_return['data']
```

#### Streamlit Folium

Streamlit Component for rendering Folium maps. Created by [@randyzwitch](https://github.com/randyzwitch).

```
m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
folium.Marker([39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell").add_to(m)

st_data = st_folium(m, width=725)
```

#### Pandas Profiling

Pandas profiling component for Streamlit. Created by [@okld](https://github.com/okld/).

```
df = pd.read_csv("https://storage.googleapis.com/tf-datasets/titanic/train.csv")
pr = df.profile_report()

st_profile_report(pr)
```

#### Image Coordinates

Get the coordinates of clicks on an image. Created by [@blackary](https://github.com/blackary/).

```
from streamlit_image_coordinates import streamlit_image_coordinates
value = streamlit_image_coordinates("https://placekitten.com/200/300")

st.write(value)
```

#### Plotly Events

Make Plotly charts interactive!. Created by [@null-jones](https://github.com/null-jones/).

```
from streamlit_plotly_events import plotly_events
fig = px.line(x=[1], y=[1])

selected_points = plotly_events(fig)
```

#### Streamlit Extras

A library with useful Streamlit extras. Created by [@arnaudmiribel](https://github.com/arnaudmiribel/).

```
from streamlit_extras.metric_cards import style_metric_cards
col3.metric(label="No Change", value=5000, delta=0)

style_metric_cards()
```

 Next

[*arrow\_back*Previous: Text elements](/develop/api-reference/text)[*arrow\_forward*Next: st.dataframe](/develop/api-reference/data/st.dataframe)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI