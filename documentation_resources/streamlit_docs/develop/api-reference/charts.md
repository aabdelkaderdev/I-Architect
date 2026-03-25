<!-- Source: https://docs.streamlit.io/develop/api-reference/charts -->

Streamlit supports several different charting libraries, and our goal is to
continually add support for more. Right now, the most basic library in our
arsenal is [Matplotlib](https://matplotlib.org/). Then there are also
interactive charting libraries like [Vega
Lite](https://vega.github.io/vega-lite/) (2D charts) and
[deck.gl](https://github.com/uber/deck.gl) (maps and 3D charts). And
finally we also provide a few chart types that are "native" to Streamlit,
like `st.line_chart` and `st.area_chart`.

[#### Simple area charts

Display an area chart.

```
st.area_chart(my_data_frame)
```](/develop/api-reference/charts/st.area_chart)[#### Simple bar charts

Display a bar chart.

```
st.bar_chart(my_data_frame)
```](/develop/api-reference/charts/st.bar_chart)[#### Simple line charts

Display a line chart.

```
st.line_chart(my_data_frame)
```](/develop/api-reference/charts/st.line_chart)[#### Simple scatter charts

Display a line chart.

```
st.scatter_chart(my_data_frame)
```](/develop/api-reference/charts/st.scatter_chart)[#### Scatterplots on maps

Display a map with points on it.

```
st.map(my_data_frame)
```](/develop/api-reference/charts/st.map)

[#### Matplotlib

Display a matplotlib.pyplot figure.

```
st.pyplot(my_mpl_figure)
```](/develop/api-reference/charts/st.pyplot)[#### Altair

Display a chart using the Altair library.

```
st.altair_chart(my_altair_chart)
```](/develop/api-reference/charts/st.altair_chart)[#### Vega-Lite

Display a chart using the Vega-Lite library.

```
st.vega_lite_chart(my_vega_lite_chart)
```](/develop/api-reference/charts/st.vega_lite_chart)[#### Plotly

Display an interactive Plotly chart.

```
st.plotly_chart(my_plotly_chart)
```](/develop/api-reference/charts/st.plotly_chart)[#### PyDeck

Display a chart using the PyDeck library.

```
st.pydeck_chart(my_pydeck_chart)
```](/develop/api-reference/charts/st.pydeck_chart)[#### GraphViz

Display a graph using the dagre-d3 library.

```
st.graphviz_chart(my_graphviz_spec)
```](/develop/api-reference/charts/st.graphviz_chart)

Third-party components

These are featured components created by our lovely community. For more examples and inspiration, check out our [Components Gallery](https://streamlit.io/components) and [Streamlit Extras](https://extras.streamlit.app)!

Previous

#### Streamlit Lottie

Integrate [Lottie](https://lottiefiles.com/) animations inside your Streamlit app. Created by [@andfanilo](https://github.com/andfanilo).

```
lottie_hello = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_V9t630.json")
st_lottie(lottie_hello, key="hello")
```

#### Plotly Events

Make Plotly charts interactive!. Created by [@null-jones](https://github.com/null-jones/).

```
fig = px.line(x=[1], y=[1])
selected_points = plotly_events(fig)
```

#### Streamlit Extras

A library with useful Streamlit extras. Created by [@arnaudmiribel](https://github.com/arnaudmiribel/).

```
chart += get_annotations_chart(annotations=[("Mar 01, 2008", "Pretty good day for GOOG"), ("Dec 01, 2007", "Something's going wrong for GOOG & AAPL"), ("Nov 01, 2008", "Market starts again thanks to..."), ("Dec 01, 2009", "Small crash for GOOG after..."),],)
st.altair_chart(chart, use_container_width=True)
```

#### Plost

A deceptively simple plotting library for Streamlit. Created by [@tvst](https://github.com/tvst).

```
import plost
plost.line_chart(my_dataframe, x='time', y='stock_value', color='stock_name',)
```

#### HiPlot

High dimensional Interactive Plotting. Created by [@facebookresearch](https://github.com/facebookresearch).

```
data = [{'dropout':0.1, 'lr': 0.001, 'loss': 10.0, 'optimizer': 'SGD'}, {'dropout':0.15, 'lr': 0.01, 'loss': 3.5, 'optimizer': 'Adam'}, {'dropout':0.3, 'lr': 0.1, 'loss': 4.5, 'optimizer': 'Adam'}]
hip.Experiment.from_iterable(data).display()
```

#### ECharts

High dimensional Interactive Plotting. Created by [@andfanilo](https://github.com/andfanilo).

```
from streamlit_echarts import st_echarts
st_echarts(options=options)
```

#### Streamlit Folium

Streamlit Component for rendering Folium maps. Created by [@randyzwitch](https://github.com/randyzwitch).

```
m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
st_data = st_folium(m, width=725)
```

#### Spacy-Streamlit

spaCy building blocks and visualizers for Streamlit apps. Created by [@explosion](https://github.com/explosion).

```
models = ["en_core_web_sm", "en_core_web_md"]
spacy_streamlit.visualize(models, "Sundar Pichai is the CEO of Google.")
```

#### Streamlit Agraph

A Streamlit Graph Vis, based on [react-grah-vis](https://github.com/crubier/react-graph-vis). Created by [@ChrisDelClea](https://github.com/ChrisDelClea).

```
from streamlit_agraph import agraph, Node, Edge, Config
agraph(nodes=nodes, edges=edges, config=config)
```

#### Streamlit Lottie

Integrate [Lottie](https://lottiefiles.com/) animations inside your Streamlit app. Created by [@andfanilo](https://github.com/andfanilo).

```
lottie_hello = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_V9t630.json")
st_lottie(lottie_hello, key="hello")
```

#### Plotly Events

Make Plotly charts interactive!. Created by [@null-jones](https://github.com/null-jones/).

```
fig = px.line(x=[1], y=[1])
selected_points = plotly_events(fig)
```

#### Streamlit Extras

A library with useful Streamlit extras. Created by [@arnaudmiribel](https://github.com/arnaudmiribel/).

```
chart += get_annotations_chart(annotations=[("Mar 01, 2008", "Pretty good day for GOOG"), ("Dec 01, 2007", "Something's going wrong for GOOG & AAPL"), ("Nov 01, 2008", "Market starts again thanks to..."), ("Dec 01, 2009", "Small crash for GOOG after..."),],)
st.altair_chart(chart, use_container_width=True)
```

#### Plost

A deceptively simple plotting library for Streamlit. Created by [@tvst](https://github.com/tvst).

```
import plost
plost.line_chart(my_dataframe, x='time', y='stock_value', color='stock_name',)
```

#### HiPlot

High dimensional Interactive Plotting. Created by [@facebookresearch](https://github.com/facebookresearch).

```
data = [{'dropout':0.1, 'lr': 0.001, 'loss': 10.0, 'optimizer': 'SGD'}, {'dropout':0.15, 'lr': 0.01, 'loss': 3.5, 'optimizer': 'Adam'}, {'dropout':0.3, 'lr': 0.1, 'loss': 4.5, 'optimizer': 'Adam'}]
hip.Experiment.from_iterable(data).display()
```

#### ECharts

High dimensional Interactive Plotting. Created by [@andfanilo](https://github.com/andfanilo).

```
from streamlit_echarts import st_echarts
st_echarts(options=options)
```

#### Streamlit Folium

Streamlit Component for rendering Folium maps. Created by [@randyzwitch](https://github.com/randyzwitch).

```
m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
st_data = st_folium(m, width=725)
```

#### Spacy-Streamlit

spaCy building blocks and visualizers for Streamlit apps. Created by [@explosion](https://github.com/explosion).

```
models = ["en_core_web_sm", "en_core_web_md"]
spacy_streamlit.visualize(models, "Sundar Pichai is the CEO of Google.")
```

#### Streamlit Agraph

A Streamlit Graph Vis, based on [react-grah-vis](https://github.com/crubier/react-graph-vis). Created by [@ChrisDelClea](https://github.com/ChrisDelClea).

```
from streamlit_agraph import agraph, Node, Edge, Config
agraph(nodes=nodes, edges=edges, config=config)
```

#### Streamlit Lottie

Integrate [Lottie](https://lottiefiles.com/) animations inside your Streamlit app. Created by [@andfanilo](https://github.com/andfanilo).

```
lottie_hello = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_V9t630.json")
st_lottie(lottie_hello, key="hello")
```

#### Plotly Events

Make Plotly charts interactive!. Created by [@null-jones](https://github.com/null-jones/).

```
fig = px.line(x=[1], y=[1])
selected_points = plotly_events(fig)
```

#### Streamlit Extras

A library with useful Streamlit extras. Created by [@arnaudmiribel](https://github.com/arnaudmiribel/).

```
chart += get_annotations_chart(annotations=[("Mar 01, 2008", "Pretty good day for GOOG"), ("Dec 01, 2007", "Something's going wrong for GOOG & AAPL"), ("Nov 01, 2008", "Market starts again thanks to..."), ("Dec 01, 2009", "Small crash for GOOG after..."),],)
st.altair_chart(chart, use_container_width=True)
```

 Next

[*arrow\_back*Previous: Data elements](/develop/api-reference/data)[*arrow\_forward*Next: st.area\_chart](/develop/api-reference/charts/st.area_chart)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI