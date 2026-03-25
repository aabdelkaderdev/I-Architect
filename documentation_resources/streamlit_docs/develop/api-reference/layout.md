<!-- Source: https://docs.streamlit.io/develop/api-reference/layout -->

Streamlit provides several options for controlling how different elements are laid out on the screen.

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

[*arrow\_back*Previous: Media elements](/develop/api-reference/media)[*arrow\_forward*Next: st.columns](/develop/api-reference/layout/st.columns)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI