<!-- Source: https://docs.streamlit.io/develop/api-reference/widgets -->

With widgets, Streamlit allows you to bake interactivity directly into your apps with buttons, sliders, text inputs, and more.

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
```](/develop/api-reference/widgets/st.page_link)

[#### Checkbox

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
```](/develop/api-reference/widgets/st.segmented_control)[#### Select slider

Display a slider widget to select items from a list.

```
size = st.select_slider("Pick a size", ["S", "M", "L"])
```](/develop/api-reference/widgets/st.select_slider)[#### Selectbox

Display a select widget.

```
choice = st.selectbox("Pick one", ["cats", "dogs"])
```](/develop/api-reference/widgets/st.selectbox)[#### Toggle

Display a toggle widget.

```
activated = st.toggle("Activate")
```](/develop/api-reference/widgets/st.toggle)

[#### Number input

Display a numeric input widget.

```
choice = st.number_input("Pick a number", 0, 10)
```](/develop/api-reference/widgets/st.number_input)[#### Slider

Display a slider widget.

```
number = st.slider("Pick a number", 0, 100)
```](/develop/api-reference/widgets/st.slider)

[#### Date input

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
```](/develop/api-reference/widgets/st.time_input)

[#### Text input

Display a single-line text input widget.

```
name = st.text_input("First name")
```](/develop/api-reference/widgets/st.text_input)[#### Text area

Display a multi-line text input widget.

```
text = st.text_area("Text to translate")
```](/develop/api-reference/widgets/st.text_area)[#### Chat input

Display a chat input widget.

```
prompt = st.chat_input("Say something")
if prompt:
    st.write(f"The user has sent: {prompt}")
```](/develop/api-reference/chat/st.chat_input)

[#### Audio input

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

[*arrow\_back*Previous: Chart elements](/develop/api-reference/charts)[*arrow\_forward*Next: st.button](/develop/api-reference/widgets/st.button)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI