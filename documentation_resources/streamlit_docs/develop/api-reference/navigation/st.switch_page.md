<!-- Source: https://docs.streamlit.io/develop/api-reference/navigation/st.switch_page -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/commands/execution_control.py#L187 "View st.switch_page source code on GitHub") | |
| --- | --- |
| st.switch\_page(page, \*, query\_params=None) | |
| Parameters | |
| page (str, Path, or st.Page) | The file path (relative to the main script) or an st.Page indicating the page to switch to. |
| query\_params (dict, list of tuples, or None) | Query parameters to apply when navigating to the target page. This can be a dictionary or an iterable of key-value tuples. Values can be strings or iterables of strings (for repeated keys). When this is None (default), all non-embed query parameters are cleared during navigation. |

#### Examples

**Example 1: Basic usage**

The following example shows how to switch to a different page in a
multipage app that uses the pages/ directory:

```
your-repository/
├── pages/
│   ├── page_1.py
│   └── page_2.py
└── your_app.py
```

```
import streamlit as st

if st.button("Home"):
    st.switch_page("your_app.py")
if st.button("Page 1"):
    st.switch_page("pages/page_1.py")
if st.button("Page 2"):
    st.switch_page("pages/page_2.py")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-switch-page.streamlit.app//?utm_medium=oembed&)

**Example 2: Passing query parameters**

The following example shows how to pass query parameters when switching to a
different page. This example uses st.navigation to create a multipage app.

```
your-repository/
├── page_2.py
└── your_app.py
```

```
import streamlit as st

def page_1():
    st.title("Page 1")
    if st.button("Switch to Page 2"):
        st.switch_page("page_2.py", query_params={"utm_source": "page_1"})

pg = st.navigation([page_1, "page_2.py"])
pg.run()
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-switch-page-query-params.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.page\_link](https://docs.streamlit.io/develop/api-reference/widgets/st.page_link)[*arrow\_forward*Next: Execution flow](/develop/api-reference/execution-flow)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI