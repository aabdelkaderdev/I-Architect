<!-- Source: https://docs.streamlit.io/develop/api-reference/configuration/st.set_option -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/config.py#L150 "View st.set_option source code on GitHub") | |
| --- | --- |
| st.set\_option(key, value) | |
| Parameters | |
| key (str) | The config option key of the form "section.optionName". To see all available options, run streamlit config show in a terminal. |
| value (null) | The new value to assign to this config option. |

#### Example

```
import streamlit as st

st.set_option("client.showErrorDetails", True)
```

[*arrow\_back*Previous: st.get\_option](/develop/api-reference/configuration/st.get_option)[*arrow\_forward*Next: st.set\_page\_config](/develop/api-reference/configuration/st.set_page_config)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI