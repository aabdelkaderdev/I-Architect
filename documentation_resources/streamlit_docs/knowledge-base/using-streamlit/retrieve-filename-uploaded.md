<!-- Source: https://docs.streamlit.io/knowledge-base/using-streamlit/retrieve-filename-uploaded -->

If you upload a single file (i.e. `accept_multiple_files=False`), the filename can be retrieved by using the `.name` attribute on the returned UploadedFile object:

```
import streamlit as st

uploaded_file = st.file_uploader("Upload a file")

if uploaded_file:
   st.write("Filename: ", uploaded_file.name)
```

If you upload multiple files (i.e. `accept_multiple_files=True`), the individual filenames can be retrieved by using the `.name` attribute on each UploadedFile object in the returned list:

```
import streamlit as st

uploaded_files = st.file_uploader("Upload multiple files", accept_multiple_files=True)

if uploaded_files:
   for uploaded_file in uploaded_files:
       st.write("Filename: ", uploaded_file.name)
```

Related forum posts:

- <https://discuss.streamlit.io/t/is-it-possible-to-get-uploaded-file-file-name/7586>

[*arrow\_back*Previous: How to remove "· Streamlit" from the app title?](/knowledge-base/using-streamlit/remove-streamlit-app-title)[*arrow\_forward*Next: Sanity checks](/knowledge-base/using-streamlit/sanity-checks)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI