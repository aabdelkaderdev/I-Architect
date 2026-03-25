<!-- Source: https://docs.streamlit.io/knowledge-base/using-streamlit/remove-streamlit-app-title -->

Using [`st.set_page_config`](/develop/api-reference/configuration/st.set_page_config) to assign the page title will not append "· Streamlit" to that title. E.g.:

```
import streamlit as st

st.set_page_config(
   page_title="Ex-stream-ly Cool App",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded",
)
```

[*arrow\_back*Previous: How can I make st.pydeck\_chart use custom Mapbox styles?](/knowledge-base/using-streamlit/pydeck-chart-custom-mapbox-styles)[*arrow\_forward*Next: How do you retrieve the filename of a file uploaded with st.file\_uploader?](/knowledge-base/using-streamlit/retrieve-filename-uploaded)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI