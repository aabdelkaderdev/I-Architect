<!-- Source: https://docs.streamlit.io/develop/api-reference/status -->

Streamlit provides a few methods that allow you to add animation to your
apps. These animations include progress bars, status messages (like
warnings), and celebratory balloons.

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
st.balloons()
```](/develop/api-reference/status/st.balloons)[#### Snowflakes

Display celebratory snowflakes!

```
st.snow()
```](/develop/api-reference/status/st.snow)

[#### Success box

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

[*arrow\_back*Previous: Chat elements](/develop/api-reference/chat)[*arrow\_forward*Next: st.success](/develop/api-reference/status/st.success)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI