<!-- Source: https://docs.streamlit.io/develop/api-reference/custom-components/st.components.v1.declare_component -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/components/v1/component_registry.py#L53 "View st.declare_component source code on GitHub") | |
| --- | --- |
| st.components.v1.declare\_component(name, path=None, url=None) | |
| Parameters | |
| name (str) | A short, descriptive name for the component, like "slider". |
| path (str, Path, or None) | The path to serve the component's frontend files from. The path should be absolute. If path is None (default), Streamlit will serve the component from the location in url. Either path or url must be specified. If both are specified, then url will take precedence. |
| url (str or None) | The URL that the component is served from. If url is None (default), Streamlit will serve the component from the location in path. Either path or url must be specified. If both are specified, then url will take precedence. |
|  |  |
| --- | --- |
| Returns | |
| (CustomComponent) | A CustomComponent that can be called like a function. Calling the component will create a new instance of the component in the Streamlit app. |

[*arrow\_back*Previous: CleanupFunction](/develop/api-reference/custom-components/component-v2-lib-cleanupfunction)[*arrow\_forward*Next: html](/develop/api-reference/custom-components/st.components.v1.html)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI