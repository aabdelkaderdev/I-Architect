<!-- Source: https://docs.streamlit.io/develop/api-reference/text/st.badge -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/markdown.py#L414 "View st.badge source code on GitHub") | |
| --- | --- |
| st.badge(label, \*, icon=None, color="blue", width="content", help=None) | |
| Parameters | |
| label (str) | The label to display in the badge. The label can optionally contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code.  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives. Because this command escapes square brackets ([ ]) in this parameter, any directive requiring square brackets is not supported. |
| icon (str or None) | An optional emoji or icon to display next to the badge label. If icon is None (default), no icon is displayed. If icon is a string, the following options are valid:   - A single-character emoji. For example, you can set icon="🚨"   or icon="🔥". Emoji short codes are not supported. - An icon from the Material Symbols library (rounded style) in the   format ":material/icon\_name:" where "icon\_name" is the name   of the icon in snake case.  For example, icon=":material/thumb\_up:" will display the   Thumb Up icon. Find additional icons in the [Material Symbols](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded)   font library. |
| color (str) | The color to use for the badge. This defaults to "blue".  This can be one of the following supported colors: red, orange, yellow, blue, green, violet, gray/grey, or primary. If you use "primary", Streamlit will use the default primary accent color unless you set the theme.primaryColor configuration option. |
| width ("content", "stretch", or int) | The width of the badge element. This can be one of the following:   - "content" (default): The width of the element matches the   width of its content, but doesn't exceed the width of the parent   container. - "stretch": The width of the element matches the width of the   parent container. - An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container. |
| help (str or None) | A tooltip to display when hovering over the badge. If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |

#### Examples

Create standalone badges with st.badge (with or without icons). If
you want to have multiple, side-by-side badges, you can use the
Markdown directive in st.markdown.

```
import streamlit as st

st.badge("New")
st.badge("Success", icon=":material/check:", color="green")

st.markdown(
    ":violet-badge[:material/star: Favorite] :orange-badge[⚠️ Needs review] :gray-badge[Deprecated]"
)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-badge.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.markdown](/develop/api-reference/text/st.markdown)[*arrow\_forward*Next: st.caption](/develop/api-reference/text/st.caption)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI