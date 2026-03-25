<!-- Source: https://docs.streamlit.io/knowledge-base/using-streamlit/insert-elements-out-of-order -->

You can use the [`st.empty`](/develop/api-reference/layout/st.empty) method as a placeholder,
to "save" a slot in your app that you can use later.

```
st.text('This will appear first')
# Appends some text to the app.

my_slot1 = st.empty()
# Appends an empty slot to the app. We'll use this later.

my_slot2 = st.empty()
# Appends another empty slot.

st.text('This will appear last')
# Appends some more text to the app.

my_slot1.text('This will appear second')
# Replaces the first empty slot with a text string.

my_slot2.line_chart(np.random.randn(20, 2))
# Replaces the second empty slot with a chart.
```

[*arrow\_back*Previous: How do I upgrade to the latest version of Streamlit?](/knowledge-base/using-streamlit/how-upgrade-latest-version-streamlit)[*arrow\_forward*Next: How can I make st.pydeck\_chart use custom Mapbox styles?](/knowledge-base/using-streamlit/pydeck-chart-custom-mapbox-styles)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI