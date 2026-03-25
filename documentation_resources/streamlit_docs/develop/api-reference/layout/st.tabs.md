<!-- Source: https://docs.streamlit.io/develop/api-reference/layout/st.tabs -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/layouts.py#L613 "View st.tabs source code on GitHub") | |
| --- | --- |
| st.tabs(tabs, \*, width="stretch", default=None, key=None, on\_change="ignore", args=None, kwargs=None) | |
| Parameters | |
| tabs (list of str) | Creates a tab for each string in the list. The first tab is selected by default. The string is used as the name of the tab and can optionally contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code, Links, and Images. Images display like icons, with a max height equal to the font height.  Unsupported Markdown elements are unwrapped so only their children (text contents) render. Common block-level Markdown (headings, lists, blockquotes) is automatically escaped and displays as literal text in labels.  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives. |
| width ("stretch" or int) | The width of the tab container. This can be one of the following:   - "stretch" (default): The width of the container matches the   width of the parent container. - An integer specifying the width in pixels: The container has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the container matches the width   of the parent container. |
| default (str or None) | The default tab to select. If this is None (default), the first tab is selected. If this is a string, it must be one of the tab labels. If two tabs have the same label as default, the first one is selected. |
| key (str, int, or None) | An optional string or integer to use as the unique key for the widget. If this is None (default), a key will be generated for the widget based on the values of the other parameters. No two widgets may have the same key.  When on\_change is set to "rerun" or a callable, setting a key lets you read or update the active tab label via st.session\_state[key]. For more details, see [Widget behavior](https://docs.streamlit.io/develop/concepts/architecture/widget-behavior). |
| on\_change ("ignore", "rerun", callable, or None) | How the tabs should respond when the user switches tabs. This controls whether tabs track state and trigger reruns. on\_change can be one of the following values:   - "ignore" (default): The tabs don't track state. All tab content   runs regardless of which tab is selected. The .open attribute   of each tab container returns None for all tabs. - "rerun": The tabs track state. Streamlit reruns the app when   the user switches tabs. The .open attribute of each tab   container returns its current state, which is True if it is   selected and False if it isn't selected. This lets you skip   expensive work in hidden tabs. - A callable: The tabs track state. Streamlit executes the callable   as a callback function and reruns the app when the user switches   tabs. The .open attribute of each tab container returns its   state like when on\_change="rerun". If you need to access   label of the current tab inside your callback, fetch it through   Session State.   When the tabs track state, they can't be used inside Streamlit cache-decorated functions. |
| args (list or tuple or None) | An optional list or tuple of args to pass to the on\_change callback. |
| kwargs (dict or None) | An optional dict of kwargs to pass to the on\_change callback. |
|  |  |
| --- | --- |
| Returns | |
| (Sequence of TabContainers) | A sequence of TabContainer objects with .open properties to return the current state of the tabs if the tabs track state. |

#### Examples

*Example 1: Use context management*

You can use with notation to insert any element into a tab:

```
import streamlit as st

tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

with tab1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-tabs1.streamlit.app//?utm_medium=oembed&)

*Example 2: Call methods directly*

You can call methods directly on the returned objects:

```
import streamlit as st
from numpy.random import default_rng as rng

df = rng(0).standard_normal((10, 1))

tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])

tab1.subheader("A tab with a chart")
tab1.line_chart(df)

tab2.subheader("A tab with the data")
tab2.write(df)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-tabs2.streamlit.app//?utm_medium=oembed&)

*Example 3: Set the default tab and style the tab labels*

Use the default parameter to set the default tab. You can also use
Markdown in the tab labels.

```
import streamlit as st

tab1, tab2, tab3 = st.tabs(
    [":cat: Cat", ":dog: Dog", ":rainbow[Owl]"], default=":rainbow[Owl]"
)

with tab1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-tabs3.streamlit.app//?utm_medium=oembed&)

**Example 4: Programmatically control the tab state**

You can use a key to programmatically control the tab state or access
the state in callbacks. You must set the on\_change parameter for
the tabs to track state.

```
import streamlit as st

def switch_tab(tab):
    st.session_state.animal = tab

def on_tab_change():
    st.toast(f"You opened the {st.session_state.animal} tab.")

cat, dog, owl = st.tabs(
    ["Cat", "Dog", "Owl"], on_change=on_tab_change, key="animal"
)

if cat.open:
    with cat:
        st.write("This is the cat")
if dog.open:
    with dog:
        st.write("This is the dog")
if owl.open:
    with owl:
        st.write("This is the owl")

with st.container(horizontal=True):
    st.button("Cat", on_click=switch_tab, args=("Cat",))
    st.button("Dog", on_click=switch_tab, args=("Dog",))
    st.button("Owl", on_click=switch_tab, args=("Owl",))
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-tabs-callback.streamlit.app//?utm_medium=oembed&)

|  |  |
| --- | --- |
| Attributes | |
| open (bool or None) | Whether this tab is the currently active tab. This is True if this tab is active and False if it is inactive, or None if state tracking isn't enabled. |

#### Examples

**Example 1: Lazy loading content**

```
import streamlit as st
import time

cat, dog, owl = st.tabs(["Cat", "Dog", "Owl"], on_change="rerun")

if cat.open:
    with cat:
        with st.spinner("Loading cat..."):
            time.sleep(2)
        st.write("This is the cat")
if dog.open:
    with dog:
        with st.spinner("Loading dog..."):
            time.sleep(2)
        st.write("This is the dog")
if owl.open:
    with owl:
        with st.spinner("Loading owl..."):
            time.sleep(2)
        st.write("This is the owl")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-tabs-lazy-load.streamlit.app//?utm_medium=oembed&)

**Example 2: Conditionally render content outside of the tab**

```
import streamlit as st

cat, dog, owl = st.tabs(["Cat", "Dog", "Owl"], on_change="rerun")

with cat:
    st.write("This is the cat")
with dog:
    st.write("This is the dog")
with owl:
    st.write("This is the owl")

if cat.open:
    options = ["orange", "tuxie", "tortie"]
    cat_color = st.sidebar.selectbox("What color is your cat?", options)
if dog.open:
    options = ["golden", "black", "white"]
    dog_color = st.sidebar.selectbox("What color is your dog?", options)
if owl.open:
    options = ["brown", "white", "black"]
    owl_color = st.sidebar.selectbox("What color is your owl?", options)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-tabs-conditional-outside.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.space](/develop/api-reference/layout/st.space)[*arrow\_forward*Next: Chat elements](/develop/api-reference/chat)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI