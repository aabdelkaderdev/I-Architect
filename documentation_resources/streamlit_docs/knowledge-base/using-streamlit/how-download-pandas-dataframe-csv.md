<!-- Source: https://docs.streamlit.io/knowledge-base/using-streamlit/how-download-pandas-dataframe-csv -->

Use the [`st.download_button`](/develop/api-reference/widgets/st.download_button) widget that is natively built into Streamlit. Check out a [sample app](https://streamlit-release-demos-0-88streamlit-app-0-88-v8ram3.streamlit.app/) demonstrating how you can use `st.download_button` to download common file formats.

```
import streamlit as st
import pandas as pd

df = pd.read_csv("dir/file.csv")

@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

csv = convert_df(df)

st.download_button(
   "Press to Download",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)
```

Additional resources:

- <https://blog.streamlit.io/0-88-0-release-notes/>
- <https://streamlit-release-demos-0-88streamlit-app-0-88-v8ram3.streamlit.app/>
- [https://docs.streamlit.io/develop/api-reference/widgets/st.download\_button](/develop/api-reference/widgets/st.download_button)

[*arrow\_back*Previous: How to download a file in Streamlit?](/knowledge-base/using-streamlit/how-download-file-streamlit)[*arrow\_forward*Next: How do I upgrade to the latest version of Streamlit?](/knowledge-base/using-streamlit/how-upgrade-latest-version-streamlit)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI