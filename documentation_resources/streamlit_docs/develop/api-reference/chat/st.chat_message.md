<!-- Source: https://docs.streamlit.io/develop/api-reference/chat/st.chat_message -->

Show API reference for

Version v1.55.0*expand\_more*

Read the [Build a basic LLM chat app](/develop/tutorials/llms/build-conversational-apps) tutorial to learn how to use `st.chat_message` and `st.chat_input` to build chat-based apps.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/widgets/chat.py#L397 "View st.chat_message source code on GitHub") | |
| --- | --- |
| st.chat\_message(name, \*, avatar=None, width="stretch") | |
| Parameters | |
| name ("user", "assistant", "ai", "human", or str) | The name of the message author. Can be "human"/"user" or "ai"/"assistant" to enable preset styling and avatars.  Currently, the name is not shown in the UI but is only set as an accessibility label. For accessibility reasons, you should not use an empty string. |
| avatar (Anything supported by st.image (except list), str, or None) | The avatar shown next to the message.  If avatar is None (default), the icon will be determined from name as follows:   - If name is "user" or "human", the message will have a   default user icon. - If name is "ai" or "assistant", the message will have   a default bot icon. - For all other values of name, the message will show the first   letter of the name.   In addition to the types supported by [st.image](https://docs.streamlit.io/develop/api-reference/media/st.image) (except list), the following strings are valid:   - A single-character emoji. For example, you can set avatar="🧑‍💻"   or avatar="🦖". Emoji short codes are not supported. - An icon from the Material Symbols library (rounded style) in the   format ":material/icon\_name:" where "icon\_name" is the name   of the icon in snake case.  For example, icon=":material/thumb\_up:" will display the   Thumb Up icon. Find additional icons in the [Material Symbols](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded)   font library. - "spinner": Displays a spinner as an icon. |
| width ("stretch", "content", or int) | The width of the chat message container. This can be one of the following:   - "stretch" (default): The width of the container matches the   width of the parent container. - "content": The width of the container matches the width of its   content, but doesn't exceed the width of the parent container. - An integer specifying the width in pixels: The container has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the container matches the width   of the parent container. |
|  |  |
| --- | --- |
| Returns | |
| (Container) | A single container that can hold multiple elements. |

#### Examples

You can use with notation to insert any element into an expander

```
import streamlit as st
import numpy as np

with st.chat_message("user"):
    st.write("Hello 👋")
    st.line_chart(np.random.randn(30, 3))
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-chat-message-user.streamlit.app//?utm_medium=oembed&)

Or you can just call methods directly in the returned objects:

```
import streamlit as st
import numpy as np

message = st.chat_message("assistant")
message.write("Hello human")
message.bar_chart(np.random.randn(30, 3))
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-chat-message-user1.streamlit.app//?utm_medium=oembed&)

For an overview of the `st.chat_message` and `st.chat_input` API, check out this video tutorial by Chanin Nantasenamat ([@dataprofessor](https://www.youtube.com/dataprofessor)), a Senior Developer Advocate at Streamlit.

[*arrow\_back*Previous: st.chat\_input](/develop/api-reference/chat/st.chat_input)[*arrow\_forward*Next: st.status](https://docs.streamlit.io/develop/api-reference/status/st.status)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI