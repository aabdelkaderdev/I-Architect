<!-- Source: https://docs.streamlit.io/knowledge-base/using-streamlit/create-anchor-link -->

Have you wanted to create anchors so that users of your app can directly navigate to specific sections by specifying `#anchor` in the URL? If so, let's find out how.

Anchors are automatically added to header text.

For example, if you define a header text via the [st.header()](/develop/api-reference/text/st.header) command as follows:

```
st.header("Section 1")
```

Then you can create a link to this header using:

```
st.markdown("[Section 1](#section-1)")
```

- Demo app: <https://dataprofessor-streamlit-anchor-app-80kk8w.streamlit.app/>
- GitHub repo: <https://github.com/dataprofessor/streamlit/blob/main/anchor_app.py>

[*arrow\_back*Previous: FAQ](/knowledge-base/using-streamlit)[*arrow\_forward*Next: Enabling camera access in your browser](/knowledge-base/using-streamlit/enable-camera)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI