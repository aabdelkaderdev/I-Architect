<!-- Source: https://docs.streamlit.io/develop/api-reference/text/st.title -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/heading.py#L255 "View st.title source code on GitHub") | |
| --- | --- |
| st.title(body, anchor=None, \*, help=None, width="stretch", text\_alignment="left") | |
| Parameters | |
| body (str) | The text to display as GitHub-flavored Markdown. Syntax information can be found at: <https://github.github.com/gfm>.  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives. |
| anchor (str or False) | The anchor name of the header that can be accessed with #anchor in the URL. If omitted, it generates an anchor using the body. If False, the anchor is not shown in the UI. |
| help (str or None) | A tooltip that gets displayed next to the title. If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| width ("stretch", "content", or int) | The width of the title element. This can be one of the following:   - "stretch" (default): The width of the element matches the   width of the parent container. - "content": The width of the element matches the width of its   content, but doesn't exceed the width of the parent container. - An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container. |
| text\_alignment ("left", "center", "right", or "justify") | The horizontal alignment of the text within the element. This can be one of the following:   - "left" (default): Text is aligned to the left edge. - "center": Text is centered. - "right": Text is aligned to the right edge. - "justify": Text is justified (stretched to fill the available   width with the last line left-aligned).   Note  For text alignment to have a visible effect, the element's width must be wider than its content. If you use width="content" with short text, the alignment may not be noticeable. |

#### Examples

```
import streamlit as st

st.title("This is a title")
st.title("_Streamlit_ is :blue[cool] :sunglasses:")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-title.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: Text elements](/develop/api-reference/text)[*arrow\_forward*Next: st.header](/develop/api-reference/text/st.header)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI