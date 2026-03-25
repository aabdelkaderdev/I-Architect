<!-- Source: https://docs.streamlit.io/develop/api-reference/layout/st.empty -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/empty.py#L28 "View st.empty source code on GitHub") | |
| --- | --- |
| st.empty() | |

#### Examples

Inside a with st.empty(): block, each displayed element will
replace the previous one.

```
import streamlit as st
import time

with st.empty():
    for seconds in range(10):
        st.write(f"⏳ {seconds} seconds have passed")
        time.sleep(1)
    st.write(":material/check: 10 seconds over!")
st.button("Rerun")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-empty.streamlit.app//?utm_medium=oembed&)

You can use an st.empty to replace multiple elements in
succession. Use st.container inside st.empty to display (and
later replace) a group of elements.

```
import streamlit as st
import time

st.button("Start over")

placeholder = st.empty()
placeholder.markdown("Hello")
time.sleep(1)

placeholder.progress(0, "Wait for it...")
time.sleep(1)
placeholder.progress(50, "Wait for it...")
time.sleep(1)
placeholder.progress(100, "Wait for it...")
time.sleep(1)

with placeholder.container():
    st.line_chart({"data": [1, 5, 2, 6]})
    time.sleep(1)
    st.markdown("3...")
    time.sleep(1)
    st.markdown("2...")
    time.sleep(1)
    st.markdown("1...")
    time.sleep(1)

placeholder.markdown("Poof!")
time.sleep(1)

placeholder.empty()
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-empty-placeholder.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.dialog](https://docs.streamlit.io/develop/api-reference/execution-flow/st.dialog)[*arrow\_forward*Next: st.expander](/develop/api-reference/layout/st.expander)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI