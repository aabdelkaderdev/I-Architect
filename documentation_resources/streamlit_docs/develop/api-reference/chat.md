<!-- Source: https://docs.streamlit.io/develop/api-reference/chat -->

Streamlit provides a few commands to help you build conversational apps. These chat elements are designed to be used in conjunction with each other, but you can also use them separately.

`st.chat_message` lets you insert a chat message container into the app so you can display messages from the user or the app. Chat containers can contain other Streamlit elements, including charts, tables, text, and more. `st.chat_input` lets you display a chat input widget so the user can type in a message. Remember to check out `st.status` to display output from long-running processes and external API calls.

[#### Chat input

Display a chat input widget.

```
prompt = st.chat_input("Say something")
if prompt:
    st.write(f"The user has sent: {prompt}")
```](/develop/api-reference/chat/st.chat_input)[#### Chat message

Insert a chat message container.

```
import numpy as np
with st.chat_message("user"):
    st.write("Hello 👋")
    st.line_chart(np.random.randn(30, 3))
```](/develop/api-reference/chat/st.chat_message)[#### Status container

Display output of long-running tasks in a container.

```
with st.status('Running'):
  do_something_slow()
```](/develop/api-reference/status/st.status)[#### st.write\_stream

Write generators or streams to the app with a typewriter effect.

```
st.write_stream(my_generator)
st.write_stream(my_llm_stream)
```](/develop/api-reference/write-magic/st.write_stream)

[*arrow\_back*Previous: Layouts and containers](/develop/api-reference/layout)[*arrow\_forward*Next: st.chat\_input](/develop/api-reference/chat/st.chat_input)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI