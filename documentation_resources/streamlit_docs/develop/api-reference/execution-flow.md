<!-- Source: https://docs.streamlit.io/develop/api-reference/execution-flow -->

By default, Streamlit apps execute the script entirely, but we allow some functionality to handle control flow in your applications.

[#### Modal dialog

Insert a modal dialog that can rerun independently from the rest of the script.

```
@st.dialog("Sign up")
def email_form():
    name = st.text_input("Name")
    email = st.text_input("Email")
```](/develop/api-reference/execution-flow/st.dialog)[#### Fragments

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

By default, Streamlit reruns your script everytime a user interacts with your app.
However, sometimes it's a better user experience to wait until a group of related
widgets is filled before actually rerunning the script. That's what `st.form` is for!

[#### Forms

Create a form that batches elements together with a “Submit" button.

```
with st.form(key='my_form'):
    name = st.text_input("Name")
    email = st.text_input("Email")
    st.form_submit_button("Sign up")
```](/develop/api-reference/execution-flow/st.form)[#### Form submit button

Display a form submit button.

```
with st.form(key='my_form'):
    name = st.text_input("Name")
    email = st.text_input("Email")
    st.form_submit_button("Sign up")
```](/develop/api-reference/execution-flow/st.form_submit_button)

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

[*arrow\_back*Previous: Navigation and pages](/develop/api-reference/navigation)[*arrow\_forward*Next: st.dialog](/develop/api-reference/execution-flow/st.dialog)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI