<!-- Source: https://docs.streamlit.io/develop/api-reference/execution-flow/st.stop -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/commands/execution_control.py#L39 "View st.stop source code on GitHub") | |
| --- | --- |
| st.stop() | |

#### Example

```
import streamlit as st

name = st.text_input("Name")
if not name:
  st.warning('Please input a name.')
  st.stop()
st.success("Thank you for inputting a name.")
```

[*arrow\_back*Previous: st.rerun](/develop/api-reference/execution-flow/st.rerun)[*arrow\_forward*Next: st.experimental\_rerun](/develop/api-reference/execution-flow/st.experimental_rerun)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI