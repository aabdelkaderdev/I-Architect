<!-- Source: https://docs.streamlit.io/develop/api-reference/media/st.logo -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/commands/logo.py#L86 "View st.logo source code on GitHub") | |
| --- | --- |
| st.logo(image, \*, size="medium", link=None, icon\_image=None) | |
| Parameters | |
| image (Anything supported by st.image (except list) or str) | The image to display in the upper-left corner of your app and its sidebar. If icon\_image is also provided, then Streamlit will only display image in the sidebar.  image can be any of the types supported by [st.image](https://docs.streamlit.io/develop/api-reference/media/st.image) except a list. Additionally, the following strings are valid:   - A single-character emoji. For example, you can set image="🏠"   or image="🚀". Emoji short codes are not supported. - An icon from the Material Symbols library (rounded style) in the   format ":material/icon\_name:" where "icon\_name" is the name   of the icon in snake case.  For example, image=":material/home:" will display the   Home icon. Find additional icons in the [Material Symbols](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded)    font library.   Streamlit scales the image to a max height set by size and a max width to fit within the sidebar. |
| size ("small", "medium", or "large") | The size of the image displayed in the upper-left corner of the app and its sidebar. The possible values are as follows:   - "small": 20px max height - "medium" (default): 24px max height - "large": 32px max height |
| link (str or None) | The external URL to open when a user clicks on the logo. The URL must start with "http://" or "https://". If link is None (default), the logo will not include a hyperlink. |
| icon\_image (Anything supported by st.image (except list), str, or None) | An optional, typically smaller image to replace image in the upper-left corner when the sidebar is closed. This can be any of the types allowed for the image parameter. If icon\_image is None (default), Streamlit will always display image in the upper-left corner, regardless of whether the sidebar is open or closed. Otherwise, Streamlit will render icon\_image in the upper-left corner of the app when the sidebar is closed.  Streamlit scales the image to a max height set by size and a max width to fit within the sidebar. If the sidebar is closed, the max width is retained from when it was last open.  For best results, pass a wide or horizontal image to image and a square image to icon\_image. Or, pass a square image to image and leave icon\_image=None. |

#### Examples

A common design practice is to use a wider logo in the sidebar, and a
smaller, icon-styled logo in your app's main body.

```
import streamlit as st

st.logo(
    LOGO_URL_LARGE,
    link="https://streamlit.io/gallery",
    icon_image=LOGO_URL_SMALL,
)
```

Try switching logos around in the following example:

```
import streamlit as st

HORIZONTAL_RED = "images/horizontal_red.png"
ICON_RED = "images/icon_red.png"
HORIZONTAL_BLUE = "images/horizontal_blue.png"
ICON_BLUE = "images/icon_blue.png"

options = [HORIZONTAL_RED, ICON_RED, HORIZONTAL_BLUE, ICON_BLUE]
sidebar_logo = st.selectbox("Sidebar logo", options, 0)
main_body_logo = st.selectbox("Main body logo", options, 1)

st.logo(sidebar_logo, icon_image=main_body_logo)
st.sidebar.markdown("Hi!")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-logo.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.image](/develop/api-reference/media/st.image)[*arrow\_forward*Next: st.pdf](/develop/api-reference/media/st.pdf)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI