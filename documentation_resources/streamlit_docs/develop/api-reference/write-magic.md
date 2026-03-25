<!-- Source: https://docs.streamlit.io/develop/api-reference/write-magic -->

Streamlit has two easy ways to display information into your app, which should typically be the
first thing you try: `st.write` and magic.

[#### st.write

Write arguments to the app.

```
st.write("Hello **world**!")
st.write(my_data_frame)
st.write(my_mpl_figure)
```](/develop/api-reference/write-magic/st.write)[#### st.write\_stream

Write generators or streams to the app with a typewriter effect.

```
st.write_stream(my_generator)
st.write_stream(my_llm_stream)
```](/develop/api-reference/write-magic/st.write_stream)[#### Magic

Any time Streamlit sees either a variable or literal value on its own line, it automatically writes that to your app using `st.write`

```
"Hello **world**!"
my_data_frame
my_mpl_figure
```](/develop/api-reference/write-magic/magic)

[*arrow\_back*Previous: API reference](/develop/api-reference)[*arrow\_forward*Next: st.write](/develop/api-reference/write-magic/st.write)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI