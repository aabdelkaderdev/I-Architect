<!-- Source: https://docs.streamlit.io/develop/api-reference/execution-flow/st.fragment -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/runtime/fragment.py#L297 "View st.fragment source code on GitHub") | |
| --- | --- |
| st.fragment(func=None, \*, run\_every=None) | |
| Parameters | |
| func (callable) | The function to turn into a fragment. |
| run\_every (int, float, timedelta, str, or None) | The time interval between automatic fragment reruns. This can be one of the following:  - None (default). - An int or float specifying the interval in seconds. - A string specifying the time in a format supported by [Pandas'   Timedelta constructor](https://pandas.pydata.org/docs/reference/api/pandas.Timedelta.html),   e.g. "1d", "1.5 days", or "1h23s". - A timedelta object from [Python's built-in datetime library](https://docs.python.org/3/library/datetime.html#timedelta-objects),   e.g. timedelta(days=1).  If run\_every is None, the fragment will only rerun from user-triggered events. |

#### Examples

The following example demonstrates basic usage of
@st.fragment. As an analogy, "inflating balloons" is a slow process that happens
outside of the fragment. "Releasing balloons" is a quick process that happens inside
of the fragment.

```
import streamlit as st
import time

@st.fragment
def release_the_balloons():
    st.button("Release the balloons", help="Fragment rerun")
    st.balloons()

with st.spinner("Inflating balloons..."):
    time.sleep(5)
release_the_balloons()
st.button("Inflate more balloons", help="Full rerun")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-fragment-balloons.streamlit.app//?utm_medium=oembed&)

This next example demonstrates how elements both inside and outside of a
fragement update with each app or fragment rerun. In this app, clicking
"Rerun full app" will increment both counters and update all values
displayed in the app. In contrast, clicking "Rerun fragment" will only
increment the counter within the fragment. In this case, the st.write
command inside the fragment will update the app's frontend, but the two
st.write commands outside the fragment will not update the frontend.

```
import streamlit as st

if "app_runs" not in st.session_state:
    st.session_state.app_runs = 0
    st.session_state.fragment_runs = 0

@st.fragment
def my_fragment():
    st.session_state.fragment_runs += 1
    st.button("Rerun fragment")
    st.write(f"Fragment says it ran {st.session_state.fragment_runs} times.")

st.session_state.app_runs += 1
my_fragment()
st.button("Rerun full app")
st.write(f"Full app says it ran {st.session_state.app_runs} times.")
st.write(f"Full app sees that fragment ran {st.session_state.fragment_runs} times.")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-fragment.streamlit.app//?utm_medium=oembed&)

You can also trigger an app rerun from inside a fragment by calling
st.rerun.

```
import streamlit as st

if "clicks" not in st.session_state:
    st.session_state.clicks = 0

@st.fragment
def count_to_five():
    if st.button("Plus one!"):
        st.session_state.clicks += 1
        if st.session_state.clicks % 5 == 0:
            st.rerun()
    return

count_to_five()
st.header(f"Multiples of five clicks: {st.session_state.clicks // 5}")

if st.button("Check click count"):
    st.toast(f"## Total clicks: {st.session_state.clicks}")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-fragment-rerun.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.form\_submit\_button](/develop/api-reference/execution-flow/st.form_submit_button)[*arrow\_forward*Next: st.rerun](/develop/api-reference/execution-flow/st.rerun)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI