<!-- Source: https://docs.streamlit.io/develop/api-reference/configuration/st.get_option -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/config.py#L199 "View st.get_option source code on GitHub") | |
| --- | --- |
| st.get\_option(key) | |
| Parameters | |
| key (str) | The config option key of the form "section.optionName". To see all available options, run streamlit config show in a terminal. |

#### Example

```
import streamlit as st

color = st.get_option("theme.primaryColor")
```

[*arrow\_back*Previous: config.toml](/develop/api-reference/configuration/config.toml)[*arrow\_forward*Next: st.set\_option](/develop/api-reference/configuration/st.set_option)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI