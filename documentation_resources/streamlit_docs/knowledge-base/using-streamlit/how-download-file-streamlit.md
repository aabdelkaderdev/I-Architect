<!-- Source: https://docs.streamlit.io/knowledge-base/using-streamlit/how-download-file-streamlit -->

Use the [`st.download_button`](/develop/api-reference/widgets/st.download_button) widget that is natively built into Streamlit. Check out a [sample app](https://streamlit-release-demos-0-88streamlit-app-0-88-v8ram3.streamlit.app/) demonstrating how you can use `st.download_button` to download common file formats.

```
import streamlit as st

# Text files

text_contents = '''
Foo, Bar
123, 456
789, 000
'''

# Different ways to use the API

st.download_button('Download CSV', text_contents, 'text/csv')
st.download_button('Download CSV', text_contents)  # Defaults to 'text/plain'

with open('myfile.csv') as f:
   st.download_button('Download CSV', f)  # Defaults to 'text/plain'

# ---
# Binary files

binary_contents = b'whatever'

# Different ways to use the API

st.download_button('Download file', binary_contents)  # Defaults to 'application/octet-stream'

with open('myfile.zip', 'rb') as f:
   st.download_button('Download Zip', f, file_name='archive.zip')  # Defaults to 'application/octet-stream'

# You can also grab the return value of the button,
# just like with any other button.

if st.download_button(...):
   st.write('Thanks for downloading!')
```

Additional resources:

- <https://blog.streamlit.io/0-88-0-release-notes/>
- <https://streamlit-release-demos-0-88streamlit-app-0-88-v8ram3.streamlit.app/>
- [https://docs.streamlit.io/develop/api-reference/widgets/st.download\_button](/develop/api-reference/widgets/st.download_button)

[*arrow\_back*Previous: Enabling camera access in your browser](/knowledge-base/using-streamlit/enable-camera)[*arrow\_forward*Next: How to download a Pandas DataFrame as a CSV?](/knowledge-base/using-streamlit/how-download-pandas-dataframe-csv)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI