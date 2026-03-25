<!-- Source: https://docs.streamlit.io/develop/api-reference/execution-flow/st.rerun -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/commands/execution_control.py#L132 "View st.rerun source code on GitHub") | |
| --- | --- |
| st.rerun(\*, scope="app") | |
| Parameters | |
| scope ("app" or "fragment") | Specifies what part of the app should rerun. If scope is "app" (default), the full app reruns. If scope is "fragment", Streamlit only reruns the fragment from which this command is called.  Setting scope="fragment" is only valid inside a fragment during a fragment rerun. If st.rerun(scope="fragment") is called during a full-app rerun or outside of a fragment, Streamlit will raise a StreamlitAPIException. |

`st.rerun` is one of the tools to control the logic of your app. While it is great for prototyping, there can be adverse side effects:

- Additional script runs may be inefficient and slower.
- Excessive reruns may complicate your app's logic and be harder to follow.
- If misused, infinite looping may crash your app.

In many cases where `st.rerun` works, [callbacks](/develop/api-reference/caching-and-state/st.session_state#use-callbacks-to-update-session-state) may be a cleaner alternative. [Containers](/develop/api-reference/layout) may also be helpful.

###### Using `st.rerun` to update an earlier header

```
import streamlit as st

if "value" not in st.session_state:
    st.session_state.value = "Title"

##### Option using st.rerun #####
st.header(st.session_state.value)

if st.button("Foo"):
    st.session_state.value = "Foo"
    st.rerun()
```

###### Using a callback to update an earlier header

```
##### Option using a callback #####
st.header(st.session_state.value)

def update_value():
    st.session_state.value = "Bar"

st.button("Bar", on_click=update_value)
```

###### Using containers to update an earlier header

```
##### Option using a container #####
container = st.container()

if st.button("Baz"):
    st.session_state.value = "Baz"

container.header(st.session_state.value)
```

[*arrow\_back*Previous: st.fragment](/develop/api-reference/execution-flow/st.fragment)[*arrow\_forward*Next: st.stop](/develop/api-reference/execution-flow/st.stop)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI