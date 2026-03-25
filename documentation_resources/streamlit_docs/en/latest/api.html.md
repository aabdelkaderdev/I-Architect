<!-- Source: https://docs.streamlit.io/en/latest/api.html -->

Streamlit makes it easy for you to visualize, mutate, and share data. The API
reference is organized by activity type, like displaying data or optimizing
performance. Each section includes methods associated with the activity type,
including examples.

Browse our API below and click to learn more about any of our available commands! 🎈

  

[#### st.write

Write arguments to the app.

```
st.write("Hello **world**!")
st.write(my_data_frame)
st.write(my_mpl_figure)
```](/develop/api-reference/write-magic/st.write)[#### st.write\_stream

Write generators or streams to the app with a typewriter effect.

```
st.write_stream(my_generator)
st.write_stream(my_llm_stream)
```](/develop/api-reference/write-magic/st.write_stream)[#### Magic

Any time Streamlit sees either a variable or literal value on its own line, it automatically writes that to your app using `st.write`

```
"Hello **world**!"
my_data_frame
my_mpl_figure
```](/develop/api-reference/write-magic/magic)

  

[#### Markdown

Display string formatted as Markdown.

```
st.markdown("Hello **world**!")
```](/develop/api-reference/text/st.markdown)[#### Title

Display text in title formatting.

```
st.title("The app title")
```](/develop/api-reference/text/st.title)[#### Header

Display text in header formatting.

```
st.header("This is a header")
```](/develop/api-reference/text/st.header)[#### Subheader

Display text in subheader formatting.

```
st.subheader("This is a subheader")
```](/develop/api-reference/text/st.subheader)[#### Badge

Display a small, colored badge.

```
st.badge("New")
```](/develop/api-reference/text/st.badge)[#### Caption

Display text in small font.

```
st.caption("This is written small caption text")
```](/develop/api-reference/text/st.caption)[#### Code block

Display a code block with optional syntax highlighting.

```
st.code("a = 1234")
```](/develop/api-reference/text/st.code)[#### Echo

Display some code in the app, then execute it. Useful for tutorials.

```
with st.echo():
  st.write('This code will be printed')
```](/develop/api-reference/text/st.echo)[#### LaTeX

Display mathematical expressions formatted as LaTeX.

```
st.latex("\int a x^2 \,dx")
```](/develop/api-reference/text/st.latex)[#### Preformatted text

Write fixed-width and preformatted text.

```
st.text("Hello world")
```](/develop/api-reference/text/st.text)[#### Divider

Display a horizontal rule.

```
st.divider()
```](/develop/api-reference/text/st.divider)[#### Get help

Display object’s doc string, nicely formatted.

```
st.help(st.write)
st.help(pd.DataFrame)
```](/develop/api-reference/text/st.help)[#### Render HTML

Renders HTML strings to your app.

```
st.html("<p>Foo bar.</p>")
```](/develop/api-reference/text/st.html)

Third-party components

These are featured components created by our lovely community. For more examples and inspiration, check out our [Components Gallery](https://streamlit.io/components) and [Streamlit Extras](https://extras.streamlit.app)!

Previous

#### Tags

Add tags to your Streamlit apps. Created by [@gagan3012](https://github.com/gagan3012).

```
st_tags(label='# Enter Keywords:', text='Press enter to add more', value=['Zero', 'One', 'Two'], suggestions=['five', 'six', 'seven', 'eight', 'nine', 'three', 'eleven', 'ten', 'four'], maxtags = 4, key='1')
```

#### NLU

Apply text mining on a dataframe. Created by [@JohnSnowLabs](https://github.com/JohnSnowLabs/).

```
nlu.load("sentiment").predict("I love NLU! <3")
```

#### Streamlit Extras

A library with useful Streamlit extras. Created by [@arnaudmiribel](https://github.com/arnaudmiribel/).

```
mention(label="An awesome Streamlit App", icon="streamlit",  url="https://extras.streamlit.app",)
```

#### Annotated text

Display annotated text in Streamlit apps. Created by [@tvst](https://github.com/tvst).

```
annotated_text("This ", ("is", "verb"), " some ", ("annotated", "adj"), ("text", "noun"), " for those of ", ("you", "pronoun"), " who ", ("like", "verb"), " this sort of ", ("thing", "noun"), ".")
```

#### Drawable Canvas

Provides a sketching canvas using [Fabric.js](http://fabricjs.com/). Created by [@andfanilo](https://github.com/andfanilo).

```
st_canvas(fill_color="rgba(255, 165, 0, 0.3)", stroke_width=stroke_width, stroke_color=stroke_color, background_color=bg_color, background_image=Image.open(bg_image) if bg_image else None, update_streamlit=realtime_update, height=150, drawing_mode=drawing_mode, point_display_radius=point_display_radius if drawing_mode == 'point' else 0, key="canvas",)
```

#### Tags

Add tags to your Streamlit apps. Created by [@gagan3012](https://github.com/gagan3012).

```
st_tags(label='# Enter Keywords:', text='Press enter to add more', value=['Zero', 'One', 'Two'], suggestions=['five', 'six', 'seven', 'eight', 'nine', 'three', 'eleven', 'ten', 'four'], maxtags = 4, key='1')
```

#### NLU

Apply text mining on a dataframe. Created by [@JohnSnowLabs](https://github.com/JohnSnowLabs/).

```
nlu.load("sentiment").predict("I love NLU! <3")
```

#### Streamlit Extras

A library with useful Streamlit extras. Created by [@arnaudmiribel](https://github.com/arnaudmiribel/).

```
mention(label="An awesome Streamlit App", icon="streamlit",  url="https://extras.streamlit.app",)
```

#### Annotated text

Display annotated text in Streamlit apps. Created by [@tvst](https://github.com/tvst).

```
annotated_text("This ", ("is", "verb"), " some ", ("annotated", "adj"), ("text", "noun"), " for those of ", ("you", "pronoun"), " who ", ("like", "verb"), " this sort of ", ("thing", "noun"), ".")
```

#### Drawable Canvas

Provides a sketching canvas using [Fabric.js](http://fabricjs.com/). Created by [@andfanilo](https://github.com/andfanilo).

```
st_canvas(fill_color="rgba(255, 165, 0, 0.3)", stroke_width=stroke_width, stroke_color=stroke_color, background_color=bg_color, background_image=Image.open(bg_image) if bg_image else None, update_streamlit=realtime_update, height=150, drawing_mode=drawing_mode, point_display_radius=point_display_radius if drawing_mode == 'point' else 0, key="canvas",)
```

#### Tags

Add tags to your Streamlit apps. Created by [@gagan3012](https://github.com/gagan3012).

```
st_tags(label='# Enter Keywords:', text='Press enter to add more', value=['Zero', 'One', 'Two'], suggestions=['five', 'six', 'seven', 'eight', 'nine', 'three', 'eleven', 'ten', 'four'], maxtags = 4, key='1')
```

#### NLU

Apply text mining on a dataframe. Created by [@JohnSnowLabs](https://github.com/JohnSnowLabs/).

```
nlu.load("sentiment").predict("I love NLU! <3")
```

#### Streamlit Extras

A library with useful Streamlit extras. Created by [@arnaudmiribel](https://github.com/arnaudmiribel/).

```
mention(label="An awesome Streamlit App", icon="streamlit",  url="https://extras.streamlit.app",)
```

 Next

  

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
```](/develop/api-reference/charts/st.map)[#### Matplotlib

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

  

[#### Button

Display a button widget.

```
clicked = st.button("Click me")
```](/develop/api-reference/widgets/st.button)[#### Download button

Display a download button widget.

```
st.download_button("Download file", file)
```](/develop/api-reference/widgets/st.download_button)[#### Form button

Display a form submit button. For use with `st.form`.

```
st.form_submit_button("Sign up")
```](/develop/api-reference/execution-flow/st.form_submit_button)[#### Link button

Display a link button.

```
st.link_button("Go to gallery", url)
```](/develop/api-reference/widgets/st.link_button)[#### Page link

Display a link to another page in a multipage app.

```
st.page_link("app.py", label="Home", icon="🏠")
st.page_link("pages/profile.py", label="My profile")
```](/develop/api-reference/widgets/st.page_link)[#### Checkbox

Display a checkbox widget.

```
selected = st.checkbox("I agree")
```](/develop/api-reference/widgets/st.checkbox)[#### Color picker

Display a color picker widget.

```
color = st.color_picker("Pick a color")
```](/develop/api-reference/widgets/st.color_picker)[#### Feedback

Display a rating or sentiment button group.

```
st.feedback("stars")
```](/develop/api-reference/widgets/st.feedback)[#### Multiselect

Display a multiselect widget. The multiselect widget starts as empty.

```
choices = st.multiselect("Buy", ["milk", "apples", "potatoes"])
```](/develop/api-reference/widgets/st.multiselect)[#### Pills

Display a pill-button selection widget.

```
st.pills("Tags", ["Sports", "AI", "Politics"])
```](/develop/api-reference/widgets/st.pills)[#### Radio

Display a radio button widget.

```
choice = st.radio("Pick one", ["cats", "dogs"])
```](/develop/api-reference/widgets/st.radio)[#### Segmented control

Display a segmented-button selection widget.

```
st.segmented_control("Filter", ["Open", "Closed", "All"])
```](/develop/api-reference/widgets/st.segmented_control)[#### Selectbox

Display a select widget.

```
choice = st.selectbox("Pick one", ["cats", "dogs"])
```](/develop/api-reference/widgets/st.selectbox)[#### Select-slider

Display a slider widget to select items from a list.

```
size = st.select_slider("Pick a size", ["S", "M", "L"])
```](/develop/api-reference/widgets/st.select_slider)[#### Toggle

Display a toggle widget.

```
activated = st.toggle("Activate")
```](/develop/api-reference/widgets/st.toggle)[#### Number input

Display a numeric input widget.

```
choice = st.number_input("Pick a number", 0, 10)
```](/develop/api-reference/widgets/st.number_input)[#### Slider

Display a slider widget.

```
number = st.slider("Pick a number", 0, 100)
```](/develop/api-reference/widgets/st.slider)[#### Date input

Display a date input widget.

```
date = st.date_input("Your birthday")
```](/develop/api-reference/widgets/st.date_input)[#### Datetime input

Display a datetime input widget.

```
datetime = st.datetime_input("Schedule your event")
```](/develop/api-reference/widgets/st.datetime_input)[#### Time input

Display a time input widget.

```
time = st.time_input("Meeting time")
```](/develop/api-reference/widgets/st.time_input)[#### Chat input

Display a chat input widget.

```
prompt = st.chat_input("Say something")
if prompt:
    st.write(f"The user has sent: {prompt}")
```](/develop/api-reference/chat/st.chat_input)[#### Text-area

Display a multi-line text input widget.

```
text = st.text_area("Text to translate")
```](/develop/api-reference/widgets/st.text_area)[#### Text input

Display a single-line text input widget.

```
name = st.text_input("First name")
```](/develop/api-reference/widgets/st.text_input)[#### Audio input

Display a widget that allows users to record with their microphone.

```
speech = st.audio_input("Record a voice message")
```](/develop/api-reference/widgets/st.audio_input)[#### Data editor

Display a data editor widget.

```
edited = st.data_editor(df, num_rows="dynamic")
```](/develop/api-reference/data/st.data_editor)[#### File uploader

Display a file uploader widget.

```
data = st.file_uploader("Upload a CSV")
```](/develop/api-reference/widgets/st.file_uploader)[#### Camera input

Display a widget that allows users to upload images directly from a camera.

```
image = st.camera_input("Take a picture")
```](/develop/api-reference/widgets/st.camera_input)

Third-party components

These are featured components created by our lovely community. For more examples and inspiration, check out our [Components Gallery](https://streamlit.io/components) and [Streamlit Extras](https://extras.streamlit.app)!

Previous

#### Streamlit Chat

Streamlit Component for a Chatbot UI. Created by [@AI-Yash](https://github.com/AI-Yash).

```
from streamlit_chat import message

message("My message")
message("Hello bot!", is_user=True)  # align's the message to the right
```

#### Streamlit Option Menu

Select a single item from a list of options in a menu. Created by [@victoryhb](https://github.com/victoryhb).

```
from streamlit_option_menu import option_menu

option_menu("Main Menu", ["Home", 'Settings'],
  icons=['house', 'gear'], menu_icon="cast", default_index=1)
```

#### Streamlit Extras

A library with useful Streamlit extras. Created by [@arnaudmiribel](https://github.com/arnaudmiribel/).

```
from streamlit_extras.stoggle import stoggle

stoggle(
    "Click me!", """🥷 Surprise! Here's some additional content""",)
```

#### Streamlit Elements

Create a draggable and resizable dashboard in Streamlit. Created by [@okls](https://github.com/okls).

```
from streamlit_elements import elements, mui, html

with elements("new_element"):
  mui.Typography("Hello world")
```

#### Tags

Add tags to your Streamlit apps. Created by [@gagan3012](https://github.com/gagan3012).

```
from streamlit_tags import st_tags

st_tags(label='# Enter Keywords:', text='Press enter to add more', value=['Zero', 'One', 'Two'],
suggestions=['five', 'six', 'seven', 'eight', 'nine', 'three', 'eleven', 'ten', 'four'], maxtags = 4, key='1')
```

#### Stqdm

The simplest way to handle a progress bar in streamlit app. Created by [@Wirg](https://github.com/Wirg).

```
from stqdm import stqdm

for _ in stqdm(range(50)):
    sleep(0.5)
```

#### Timeline

Display a Timeline in Streamlit apps using [TimelineJS](https://timeline.knightlab.com/). Created by [@innerdoc](https://github.com/innerdoc).

```
from streamlit_timeline import timeline

with open('example.json', "r") as f:
  timeline(f.read(), height=800)
```

#### Camera input live

Alternative for st.camera\_input which returns the webcam images live. Created by [@blackary](https://github.com/blackary).

```
from camera_input_live import camera_input_live

image = camera_input_live()
st.image(value)
```

#### Streamlit Ace

Ace editor component for Streamlit. Created by [@okld](https://github.com/okld).

```
from streamlit_ace import st_ace

content = st_ace()
content
```

#### Streamlit Chat

Streamlit Component for a Chatbot UI. Created by [@AI-Yash](https://github.com/AI-Yash).

```
from streamlit_chat import message

message("My message")
message("Hello bot!", is_user=True)  # align's the message to the right
```

#### Streamlit Option Menu

Select a single item from a list of options in a menu. Created by [@victoryhb](https://github.com/victoryhb).

```
from streamlit_option_menu import option_menu

option_menu("Main Menu", ["Home", 'Settings'],
  icons=['house', 'gear'], menu_icon="cast", default_index=1)
```

#### Streamlit Extras

A library with useful Streamlit extras. Created by [@arnaudmiribel](https://github.com/arnaudmiribel/).

```
from streamlit_extras.stoggle import stoggle

stoggle(
    "Click me!", """🥷 Surprise! Here's some additional content""",)
```

#### Streamlit Elements

Create a draggable and resizable dashboard in Streamlit. Created by [@okls](https://github.com/okls).

```
from streamlit_elements import elements, mui, html

with elements("new_element"):
  mui.Typography("Hello world")
```

#### Tags

Add tags to your Streamlit apps. Created by [@gagan3012](https://github.com/gagan3012).

```
from streamlit_tags import st_tags

st_tags(label='# Enter Keywords:', text='Press enter to add more', value=['Zero', 'One', 'Two'],
suggestions=['five', 'six', 'seven', 'eight', 'nine', 'three', 'eleven', 'ten', 'four'], maxtags = 4, key='1')
```

#### Stqdm

The simplest way to handle a progress bar in streamlit app. Created by [@Wirg](https://github.com/Wirg).

```
from stqdm import stqdm

for _ in stqdm(range(50)):
    sleep(0.5)
```

#### Timeline

Display a Timeline in Streamlit apps using [TimelineJS](https://timeline.knightlab.com/). Created by [@innerdoc](https://github.com/innerdoc).

```
from streamlit_timeline import timeline

with open('example.json', "r") as f:
  timeline(f.read(), height=800)
```

#### Camera input live

Alternative for st.camera\_input which returns the webcam images live. Created by [@blackary](https://github.com/blackary).

```
from camera_input_live import camera_input_live

image = camera_input_live()
st.image(value)
```

#### Streamlit Ace

Ace editor component for Streamlit. Created by [@okld](https://github.com/okld).

```
from streamlit_ace import st_ace

content = st_ace()
content
```

#### Streamlit Chat

Streamlit Component for a Chatbot UI. Created by [@AI-Yash](https://github.com/AI-Yash).

```
from streamlit_chat import message

message("My message")
message("Hello bot!", is_user=True)  # align's the message to the right
```

#### Streamlit Option Menu

Select a single item from a list of options in a menu. Created by [@victoryhb](https://github.com/victoryhb).

```
from streamlit_option_menu import option_menu

option_menu("Main Menu", ["Home", 'Settings'],
  icons=['house', 'gear'], menu_icon="cast", default_index=1)
```

#### Streamlit Extras

A library with useful Streamlit extras. Created by [@arnaudmiribel](https://github.com/arnaudmiribel/).

```
from streamlit_extras.stoggle import stoggle

stoggle(
    "Click me!", """🥷 Surprise! Here's some additional content""",)
```

 Next

  

[#### Image

Display an image or list of images.

```
st.image(numpy_array)
st.image(image_bytes)
st.image(file)
st.image("https://example.com/myimage.jpg")
```](/develop/api-reference/media/st.image)[#### Logo

Display a logo in the upper-left corner of your app and its sidebar.

```
st.logo("logo.jpg")
```](/develop/api-reference/media/st.logo)[#### PDF

Display a PDF file.

```
st.pdf("my_document.pdf")
```](/develop/api-reference/media/st.pdf)[#### Audio

Display an audio player.

```
st.audio(numpy_array)
st.audio(audio_bytes)
st.audio(file)
st.audio("https://example.com/myaudio.mp3", format="audio/mp3")
```](/develop/api-reference/media/st.audio)[#### Video

Display a video player.

```
st.video(numpy_array)
st.video(video_bytes)
st.video(file)
st.video("https://example.com/myvideo.mp4", format="video/mp4")
```](/develop/api-reference/media/st.video)

Third-party components

These are featured components created by our lovely community. For more examples and inspiration, check out our [Components Gallery](https://streamlit.io/components) and [Streamlit Extras](https://extras.streamlit.app)!

Previous

#### Streamlit Cropper

A simple image cropper for Streamlit. Created by [@turner-anderson](https://github.com/turner-anderson).

```
from streamlit_cropper import st_cropper

st_cropper(img, realtime_update=realtime_update, box_color=box_color, aspect_ratio=aspect_ratio)
```

#### Image Coordinates

Get the coordinates of clicks on an image. Created by [@blackary](https://github.com/blackary/).

```
from streamlit_image_coordinates import streamlit_image_coordinates

streamlit_image_coordinates("https://placekitten.com/200/300")
```

#### Streamlit Lottie

Integrate [Lottie](https://lottiefiles.com/) animations inside your Streamlit app. Created by [@andfanilo](https://github.com/andfanilo).

```
lottie_hello = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_V9t630.json")

st_lottie(lottie_hello, key="hello")
```

#### Streamlit Webrtc

Handling and transmitting real-time video/audio streams with Streamlit. Created by [@whitphx](https://github.com/whitphx).

```
from streamlit_webrtc import webrtc_streamer

webrtc_streamer(key="sample")
```

#### Drawable Canvas

Provides a sketching canvas using [Fabric.js](http://fabricjs.com/). Created by [@andfanilo](https://github.com/andfanilo).

```
from streamlit_drawable_canvas import st_canvas

st_canvas(fill_color="rgba(255, 165, 0, 0.3)", stroke_width=stroke_width, stroke_color=stroke_color, background_color=bg_color, background_image=Image.open(bg_image) if bg_image else None, update_streamlit=realtime_update, height=150, drawing_mode=drawing_mode, point_display_radius=point_display_radius if drawing_mode == 'point' else 0, key="canvas",)
```

#### Image Comparison

Compare images with a slider using [JuxtaposeJS](https://juxtapose.knightlab.com/). Created by [@fcakyon](https://github.com/fcakyon).

```
from streamlit_image_comparison import image_comparison

image_comparison(img1="image1.jpg", img2="image2.jpg",)
```

#### Streamlit Cropper

A simple image cropper for Streamlit. Created by [@turner-anderson](https://github.com/turner-anderson).

```
from streamlit_cropper import st_cropper

st_cropper(img, realtime_update=realtime_update, box_color=box_color, aspect_ratio=aspect_ratio)
```

#### Image Coordinates

Get the coordinates of clicks on an image. Created by [@blackary](https://github.com/blackary/).

```
from streamlit_image_coordinates import streamlit_image_coordinates

streamlit_image_coordinates("https://placekitten.com/200/300")
```

#### Streamlit Lottie

Integrate [Lottie](https://lottiefiles.com/) animations inside your Streamlit app. Created by [@andfanilo](https://github.com/andfanilo).

```
lottie_hello = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_V9t630.json")

st_lottie(lottie_hello, key="hello")
```

#### Streamlit Webrtc

Handling and transmitting real-time video/audio streams with Streamlit. Created by [@whitphx](https://github.com/whitphx).

```
from streamlit_webrtc import webrtc_streamer

webrtc_streamer(key="sample")
```

#### Drawable Canvas

Provides a sketching canvas using [Fabric.js](http://fabricjs.com/). Created by [@andfanilo](https://github.com/andfanilo).

```
from streamlit_drawable_canvas import st_canvas

st_canvas(fill_color="rgba(255, 165, 0, 0.3)", stroke_width=stroke_width, stroke_color=stroke_color, background_color=bg_color, background_image=Image.open(bg_image) if bg_image else None, update_streamlit=realtime_update, height=150, drawing_mode=drawing_mode, point_display_radius=point_display_radius if drawing_mode == 'point' else 0, key="canvas",)
```

#### Image Comparison

Compare images with a slider using [JuxtaposeJS](https://juxtapose.knightlab.com/). Created by [@fcakyon](https://github.com/fcakyon).

```
from streamlit_image_comparison import image_comparison

image_comparison(img1="image1.jpg", img2="image2.jpg",)
```

#### Streamlit Cropper

A simple image cropper for Streamlit. Created by [@turner-anderson](https://github.com/turner-anderson).

```
from streamlit_cropper import st_cropper

st_cropper(img, realtime_update=realtime_update, box_color=box_color, aspect_ratio=aspect_ratio)
```

#### Image Coordinates

Get the coordinates of clicks on an image. Created by [@blackary](https://github.com/blackary/).

```
from streamlit_image_coordinates import streamlit_image_coordinates

streamlit_image_coordinates("https://placekitten.com/200/300")
```

#### Streamlit Lottie

Integrate [Lottie](https://lottiefiles.com/) animations inside your Streamlit app. Created by [@andfanilo](https://github.com/andfanilo).

```
lottie_hello = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_V9t630.json")

st_lottie(lottie_hello, key="hello")
```

 Next

  

[#### Columns

Insert containers laid out as side-by-side columns.

```
col1, col2 = st.columns(2)
col1.write("this is column 1")
col2.write("this is column 2")
```](/develop/api-reference/layout/st.columns)[#### Container

Insert a multi-element container.

```
c = st.container()
st.write("This will show last")
c.write("This will show first")
c.write("This will show second")
```](/develop/api-reference/layout/st.container)[#### Modal dialog

Insert a modal dialog that can rerun independently from the rest of the script.

```
@st.dialog("Sign up")
def email_form():
    name = st.text_input("Name")
    email = st.text_input("Email")
```](/develop/api-reference/execution-flow/st.dialog)[#### Empty

Insert a single-element container.

```
c = st.empty()
st.write("This will show last")
c.write("This will be replaced")
c.write("This will show first")
```](/develop/api-reference/layout/st.empty)[#### Expander

Insert a multi-element container that can be expanded/collapsed.

```
with st.expander("Open to see more"):
  st.write("This is more content")
```](/develop/api-reference/layout/st.expander)[#### Popover

Insert a multi-element popover container that can be opened/closed.

```
with st.popover("Settings"):
  st.checkbox("Show completed")
```](/develop/api-reference/layout/st.popover)[#### Sidebar

Display items in a sidebar.

```
st.sidebar.write("This lives in the sidebar")
st.sidebar.button("Click me!")
```](/develop/api-reference/layout/st.sidebar)[#### Space

Add vertical or horizontal space.

```
st.space("small")
```](/develop/api-reference/layout/st.space)[#### Tabs

Insert containers separated into tabs.

```
tab1, tab2 = st.tabs(["Tab 1", "Tab2"])
tab1.write("this is tab 1")
tab2.write("this is tab 2")
```](/develop/api-reference/layout/st.tabs)

Third-party components

These are featured components created by our lovely community. For more examples and inspiration, check out our [Components Gallery](https://streamlit.io/components) and [Streamlit Extras](https://extras.streamlit.app)!

#### Streamlit Elements

Create a draggable and resizable dashboard in Streamlit. Created by [@okls](https://github.com/okls).

```
from streamlit_elements import elements, mui, html

with elements("new_element"):
  mui.Typography("Hello world")
```

#### Pydantic

Auto-generate Streamlit UI from Pydantic Models and Dataclasses. Created by [@lukasmasuch](https://github.com/lukasmasuch).

```
import streamlit_pydantic as sp

sp.pydantic_form(key="my_form",
  model=ExampleModel)
```

#### Streamlit Pages

An experimental version of Streamlit Multi-Page Apps. Created by [@blackary](https://github.com/blackary).

```
from st_pages import Page, show_pages, add_page_title

show_pages([ Page("streamlit_app.py", "Home", "🏠"),
  Page("other_pages/page2.py", "Page 2", ":books:"), ])
```

  

Streamlit provides a few commands to help you build conversational apps. These chat elements are designed to be used in conjunction with each other, but you can also use them separately.

`st.chat_message` lets you insert a chat message container into the app so you can display messages from the user or the app. Chat containers can contain other Streamlit elements, including charts, tables, text, and more. `st.chat_input` lets you display a chat input widget so the user can type in a message.

[#### Chat input

Display a chat input widget.

```
prompt = st.chat_input("Say something")
if prompt:
    st.write(f"The user has sent: {prompt}")
```](/develop/api-reference/chat/st.chat_input)[#### Chat message

Insert a chat message container.

```
import numpy as np
with st.chat_message("user"):
    st.write("Hello 👋")
    st.line_chart(np.random.randn(30, 3))
```](/develop/api-reference/chat/st.chat_message)[#### Status container

Display output of long-running tasks in a container.

```
with st.status('Running'):
  do_something_slow()
```](/develop/api-reference/status/st.status)[#### st.write\_stream

Write generators or streams to the app with a typewriter effect.

```
st.write_stream(my_generator)
st.write_stream(my_llm_stream)
```](/develop/api-reference/write-magic/st.write_stream)

  

[#### Progress bar

Display a progress bar.

```
for i in range(101):
  st.progress(i)
  do_something_slow()
```](/develop/api-reference/status/st.progress)[#### Spinner

Temporarily displays a message while executing a block of code.

```
with st.spinner("Please wait..."):
  do_something_slow()
```](/develop/api-reference/status/st.spinner)[#### Status container

Display output of long-running tasks in a container.

```
with st.status('Running'):
  do_something_slow()
```](/develop/api-reference/status/st.status)[#### Toast

Briefly displays a toast message in the bottom-right corner.

```
st.toast('Butter!', icon='🧈')
```](/develop/api-reference/status/st.toast)[#### Balloons

Display celebratory balloons!

```
do_something()

# Celebrate when all done!
st.balloons()
```](/develop/api-reference/status/st.balloons)[#### Snowflakes

Display celebratory snowflakes!

```
do_something()

# Celebrate when all done!
st.snow()
```](/develop/api-reference/status/st.snow)[#### Success box

Display a success message.

```
st.success("Match found!")
```](/develop/api-reference/status/st.success)[#### Info box

Display an informational message.

```
st.info("Dataset is updated every day at midnight.")
```](/develop/api-reference/status/st.info)[#### Warning box

Display warning message.

```
st.warning("Unable to fetch image. Skipping...")
```](/develop/api-reference/status/st.warning)[#### Error box

Display error message.

```
st.error("We encountered an error")
```](/develop/api-reference/status/st.error)[#### Exception output

Display an exception.

```
e = RuntimeError("This is an exception of type RuntimeError")
st.exception(e)
```](/develop/api-reference/status/st.exception)

Third-party components

These are featured components created by our lovely community. For more examples and inspiration, check out our [Components Gallery](https://streamlit.io/components) and [Streamlit Extras](https://extras.streamlit.app)!

#### Stqdm

The simplest way to handle a progress bar in streamlit app. Created by [@Wirg](https://github.com/Wirg).

```
from stqdm import stqdm

for _ in stqdm(range(50)):
    sleep(0.5)
```

#### Custom notification box

A custom notification box with the ability to close it out. Created by [@Socvest](https://github.com/Socvest).

```
from streamlit_custom_notification_box import custom_notification_box

styles = {'material-icons':{'color': 'red'}, 'text-icon-link-close-container': {'box-shadow': '#3896de 0px 4px'}, 'notification-text': {'':''}, 'close-button':{'':''}, 'link':{'':''}}
custom_notification_box(icon='info', textDisplay='We are almost done with your registration...', externalLink='more info', url='#', styles=styles, key="foo")
```

#### Streamlit Extras

A library with useful Streamlit extras. Created by [@arnaudmiribel](https://github.com/arnaudmiribel/).

```
from streamlit_extras.let_it_rain import rain

rain(emoji="🎈", font_size=54,
  falling_speed=5, animation_length="infinite",)
```

  

[#### Log in a user

`st.login()` starts an authentication flow with an identity provider.

```
st.login()
```](/develop/api-reference/user/st.login)[#### Log out a user

`st.logout()` removes a user's identity information.

```
st.logout()
```](/develop/api-reference/user/st.logout)[#### User info

`st.user` returns information about a logged-in user.

```
if st.user.is_logged_in:
  st.write(f"Welcome back, {st.user.name}!")
```](/develop/api-reference/user/st.user)

  

[#### Navigation

Configure the available pages in a multipage app.

```
st.navigation({
    "Your account" : [log_out, settings],
    "Reports" : [overview, usage],
    "Tools" : [search]
})
```](/develop/api-reference/navigation/st.navigation)[#### Page

Define a page in a multipage app.

```
home = st.Page(
    "home.py",
    title="Home",
    icon=":material/home:"
)
```](/develop/api-reference/navigation/st.page)[#### Page link

Display a link to another page in a multipage app.

```
st.page_link("app.py", label="Home", icon="🏠")
st.page_link("pages/profile.py", label="My profile")
```](/develop/api-reference/widgets/st.page_link)[#### Switch page

Programmatically navigates to a specified page.

```
st.switch_page("pages/my_page.py")
```](/develop/api-reference/navigation/st.switch_page)

  

[#### Modal dialog

Insert a modal dialog that can rerun independently from the rest of the script.

```
@st.dialog("Sign up")
def email_form():
    name = st.text_input("Name")
    email = st.text_input("Email")
```](/develop/api-reference/execution-flow/st.dialog)[#### Forms

Create a form that batches elements together with a “Submit" button.

```
with st.form(key='my_form'):
    name = st.text_input("Name")
    email = st.text_input("Email")
    st.form_submit_button("Sign up")
```](/develop/api-reference/execution-flow/st.form)[#### Fragments

Define a fragment to rerun independently from the rest of the script.

```
@st.fragment(run_every="10s")
def fragment():
    df = get_data()
    st.line_chart(df)
```](/develop/api-reference/execution-flow/st.fragment)[#### Rerun script

Rerun the script immediately.

```
st.rerun()
```](/develop/api-reference/execution-flow/st.rerun)[#### Stop execution

Stops execution immediately.

```
st.stop()
```](/develop/api-reference/execution-flow/st.stop)

Third-party components

These are featured components created by our lovely community. For more examples and inspiration, check out our [Components Gallery](https://streamlit.io/components) and [Streamlit Extras](https://extras.streamlit.app)!

#### Autorefresh

Force a refresh without tying up a script. Created by [@kmcgrady](https://github.com/kmcgrady).

```
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=2000, limit=100,
  key="fizzbuzzcounter")
```

#### Pydantic

Auto-generate Streamlit UI from Pydantic Models and Dataclasses. Created by [@lukasmasuch](https://github.com/lukasmasuch).

```
import streamlit_pydantic as sp

sp.pydantic_form(key="my_form",
  model=ExampleModel)
```

#### Streamlit Pages

An experimental version of Streamlit Multi-Page Apps. Created by [@blackary](https://github.com/blackary).

```
from st_pages import Page, show_pages, add_page_title

show_pages([ Page("streamlit_app.py", "Home", "🏠"),
  Page("other_pages/page2.py", "Page 2", ":books:"), ])
```

  

[#### Cache data

Function decorator to cache functions that return data (e.g. dataframe transforms, database queries, ML inference).

```
@st.cache_data
def long_function(param1, param2):
  # Perform expensive computation here or
  # fetch data from the web here
  return data
```](/develop/api-reference/caching-and-state/st.cache_data)[#### Cache resource

Function decorator to cache functions that return global resources (e.g. database connections, ML models).

```
@st.cache_resource
def init_model():
  # Return a global resource here
  return pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
  )
```](/develop/api-reference/caching-and-state/st.cache_resource)[#### Session state

Session state is a way to share variables between reruns, for each user session.

```
st.session_state['key'] = value
```](/develop/api-reference/caching-and-state/st.session_state)[#### Query parameters

Get, set, or clear the query parameters that are shown in the browser's URL bar.

```
st.query_params[key] = value
st.query_params.clear()
```](/develop/api-reference/caching-and-state/st.query_params)[#### Context

`st.context` provides a read-only interface to access cookies, headers, locale, and other browser-session information.

```
st.context.cookies
st.context.headers
```](/develop/api-reference/caching-and-state/st.context)

#### Setup your connection

[#### Create a connection

Connect to a data source or API

```
conn = st.connection('pets_db', type='sql')
pet_owners = conn.query('select * from pet_owners')
st.dataframe(pet_owners)
```](/develop/api-reference/connections/st.connection)

#### Built-in connections

[#### SnowflakeConnection

A connection to Snowflake.

```
conn = st.connection('snowflake')
```](/develop/api-reference/connections/st.connections.snowflakeconnection)[#### SQLConnection

A connection to a SQL database using SQLAlchemy.

```
conn = st.connection('sql')
```](/develop/api-reference/connections/st.connections.sqlconnection)

#### Build your own connections

[#### Connection base class

Build your own connection with `BaseConnection`.

```
class MyConnection(BaseConnection[myconn.MyConnection]):
    def _connect(self, **kwargs) -> MyConnection:
        return myconn.connect(**self._secrets, **kwargs)
    def query(self, query):
        return self._instance.query(query)
```](/develop/api-reference/connections/st.connections.baseconnection)

#### Secrets management

[#### Secrets singleton

Access secrets from a local TOML file.

```
key = st.secrets["OpenAI_key"]
```](/develop/api-reference/connections/st.secrets)[#### Secrets file

Save your secrets in a per-project or per-profile TOML file.

```
OpenAI_key = "<YOUR_SECRET_KEY>"
```](/develop/api-reference/connections/secrets.toml)

Third-party components

These are featured components created by our lovely community. For more examples and inspiration, check out our [Components Gallery](https://streamlit.io/components) and [Streamlit Extras](https://extras.streamlit.app)!

#### Authenticator

A secure authentication module to validate user credentials. Created by [@mkhorasani](https://github.com/mkhorasani).

```
import streamlit_authenticator as stauth

authenticator = stauth.Authenticate( config['credentials'], config['cookie']['name'],
config['cookie']['key'], config['cookie']['expiry_days'], config['preauthorized'])
```

#### WS localStorage

A simple synchronous way of accessing localStorage from your app. Created by [@gagangoku](https://github.com/gagangoku).

```
from streamlit_ws_localstorage import injectWebsocketCode

ret = conn.setLocalStorageVal(key='k1', val='v1')
st.write('ret: ' + ret)
```

#### Streamlit Auth0

The fastest way to provide comprehensive login inside Streamlit. Created by [@conradbez](https://github.com/conradbez).

```
from auth0_component import login_button

user_info = login_button(clientId, domain = domain)
st.write(user_info)
```

  

#### V2 custom components

[#### Register

Register a custom component.

```
my_component = st.components.v2.component(
    html=HTML,
    js=JS
)
my_component()
```](/develop/api-reference/custom-components/st.components.v2.component)[#### Mount

Mount a custom component.

```
my_component = st.components.v2.component(
    html=HTML,
    js=JS
)
my_component()
```](/develop/api-reference/custom-components/st.components.v2.types.componentrenderer)[#### npm support code

Support code published through npm.

```
npm i @streamlit/component-v2-lib
```](/develop/api-reference/custom-components/component-v2-lib)[#### FrontendRenderer

Type alias for the component function.

```
import { FrontendRenderer } from "@streamlit/component-v2-lib";
```](/develop/api-reference/custom-components/component-v2-lib-frontendrenderer)[#### FrontendRendererArgs

Type alias for the component arguments.

```
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
```](/develop/api-reference/custom-components/component-v2-lib-frontendrendererargs)[#### FrontendState

Type alias for the component state.

```
import { FrontendState } from "@streamlit/component-v2-lib";
```](/develop/api-reference/custom-components/component-v2-lib-frontendstate)[#### CleanupFunction

Type alias for the component cleanup function.

```
import { CleanupFunction } from "@streamlit/component-v2-lib";
```](/develop/api-reference/custom-components/component-v2-lib-cleanupfunction)

#### V1 custom components

[#### Declare a component

Create and register a custom component.

```
from st.components.v1 import declare_component
declare_component(
    "custom_slider",
    "/frontend",
)
```](/develop/api-reference/custom-components/st.components.v1.declare_component)[#### HTML

Display an HTML string in an iframe.

```
from st.components.v1 import html
html(
    "<p>Foo bar.</p>"
)
```](/develop/api-reference/custom-components/st.components.v1.html)[#### iframe

Load a remote URL in an iframe.

```
from st.components.v1 import iframe
iframe(
    "docs.streamlit.io"
)
```](/develop/api-reference/custom-components/st.components.v1.iframe)

  

[#### Configuration file

Configures the default settings for your app.

```
your-project/
├── .streamlit/
│   └── config.toml
└── your_app.py
```](/develop/api-reference/configuration/config.toml)[#### Get config option

Retrieve a single configuration option.

```
st.get_option("theme.primaryColor")
```](/develop/api-reference/configuration/st.get_option)[#### Set config option

Set a single configuration option. (This is very limited.)

```
st.set_option("deprecation.showPyplotGlobalUse", False)
```](/develop/api-reference/configuration/st.set_option)[#### Set page title, favicon, and more

Configures the default settings of the page.

```
st.set_page_config(
  page_title="My app",
  page_icon=":shark:",
)
```](/develop/api-reference/configuration/st.set_page_config)

  

[#### st.testing.v1.AppTest

`st.testing.v1.AppTest` simulates a running Streamlit app for testing.

```
from streamlit.testing.v1 import AppTest

at = AppTest.from_file("streamlit_app.py")
at.secrets["WORD"] = "Foobar"
at.run()
assert not at.exception

at.text_input("word").input("Bazbat").run()
assert at.warning[0].value == "Try again."
```](/develop/api-reference/app-testing/st.testing.v1.apptest)[#### AppTest.from\_file

`st.testing.v1.AppTest.from_file` initializes a simulated app from a file.

```
from streamlit.testing.v1 import AppTest

at = AppTest.from_file("streamlit_app.py")
at.run()
```](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestfrom_file)[#### AppTest.from\_string

`st.testing.v1.AppTest.from_string` initializes a simulated app from a string.

```
from streamlit.testing.v1 import AppTest

at = AppTest.from_string(app_script_as_string)
at.run()
```](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestfrom_string)[#### AppTest.from\_function

`st.testing.v1.AppTest.from_function` initializes a simulated app from a function.

```
from streamlit.testing.v1 import AppTest

at = AppTest.from_function(app_script_as_callable)
at.run()
```](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestfrom_function)[#### Block

A representation of container elements, including:

- `st.chat_message`
- `st.columns`
- `st.sidebar`
- `st.tabs`
- The main body of the app.

```
# at.sidebar returns a Block
at.sidebar.button[0].click().run()
assert not at.exception
```](/develop/api-reference/app-testing/testing-element-classes#sttestingv1element_treeblock)[#### Element

The base class for representation of all elements, including:

- `st.title`
- `st.header`
- `st.markdown`
- `st.dataframe`

```
# at.title returns a sequence of Title
# Title inherits from Element
assert at.title[0].value == "My awesome app"
```](/develop/api-reference/app-testing/testing-element-classes#sttestingv1element_treeelement)[#### Button

A representation of `st.button` and `st.form_submit_button`.

```
at.button[0].click().run()
```](/develop/api-reference/app-testing/testing-element-classes#sttestingv1element_treebutton)[#### ChatInput

A representation of `st.chat_input`.

```
at.chat_input[0].set_value("What is Streamlit?").run()
```](/develop/api-reference/app-testing/testing-element-classes#sttestingv1element_treechatinput)[#### Checkbox

A representation of `st.checkbox`.

```
at.checkbox[0].check().run()
```](/develop/api-reference/app-testing/testing-element-classes#sttestingv1element_treecheckbox)[#### ColorPicker

A representation of `st.color_picker`.

```
at.color_picker[0].pick("#FF4B4B").run()
```](/develop/api-reference/app-testing/testing-element-classes#sttestingv1element_treecolorpicker)[#### DateInput

A representation of `st.date_input`.

```
release_date = datetime.date(2023, 10, 26)
at.date_input[0].set_value(release_date).run()
```](/develop/api-reference/app-testing/testing-element-classes#sttestingv1element_treedateinput)[#### Multiselect

A representation of `st.multiselect`.

```
at.multiselect[0].select("New York").run()
```](/develop/api-reference/app-testing/testing-element-classes#sttestingv1element_treemultiselect)[#### NumberInput

A representation of `st.number_input`.

```
at.number_input[0].increment().run()
```](/develop/api-reference/app-testing/testing-element-classes#sttestingv1element_treenumberinput)[#### Radio

A representation of `st.radio`.

```
at.radio[0].set_value("New York").run()
```](/develop/api-reference/app-testing/testing-element-classes#sttestingv1element_treeradio)[#### SelectSlider

A representation of `st.select_slider`.

```
at.select_slider[0].set_range("A","C").run()
```](/develop/api-reference/app-testing/testing-element-classes#sttestingv1element_treeselectslider)[#### Selectbox

A representation of `st.selectbox`.

```
at.selectbox[0].select("New York").run()
```](/develop/api-reference/app-testing/testing-element-classes#sttestingv1element_treeselectbox)[#### Slider

A representation of `st.slider`.

```
at.slider[0].set_range(2,5).run()
```](/develop/api-reference/app-testing/testing-element-classes#sttestingv1element_treeslider)[#### TextArea

A representation of `st.text_area`.

```
at.text_area[0].input("Streamlit is awesome!").run()
```](/develop/api-reference/app-testing/testing-element-classes#sttestingv1element_treetextarea)[#### TextInput

A representation of `st.text_input`.

```
at.text_input[0].input("Streamlit").run()
```](/develop/api-reference/app-testing/testing-element-classes#sttestingv1element_treetextinput)[#### TimeInput

A representation of `st.time_input`.

```
at.time_input[0].increment().run()
```](/develop/api-reference/app-testing/testing-element-classes#sttestingv1element_treetimeinput)[#### Toggle

A representation of `st.toggle`.

```
at.toggle[0].set_value("True").run()
```](/develop/api-reference/app-testing/testing-element-classes#sttestingv1element_treetoggle)

Third-party components

These are featured components created by our lovely community. For more examples and inspiration, check out our [Components Gallery](https://streamlit.io/components) and [Streamlit Extras](https://extras.streamlit.app)!

#### Pandas Profiling

Pandas profiling component for Streamlit. Created by [@okld](https://github.com/okld/).

```
df = pd.read_csv("https://storage.googleapis.com/tf-datasets/titanic/train.csv")
pr = df.profile_report()

st_profile_report(pr)
```

#### Streamlit Ace

Ace editor component for Streamlit. Created by [@okld](https://github.com/okld).

```
from streamlit_ace import st_ace

content = st_ace()
content
```

#### Streamlit Analytics

Track & visualize user interactions with your streamlit app. Created by [@jrieke](https://github.com/jrieke).

```
import streamlit_analytics

with streamlit_analytics.track():
    st.text_input("Write something")
```

[*arrow\_back*Previous: Concepts](/develop/concepts)[*arrow\_forward*Next: Write and magic](/develop/api-reference/write-magic)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI