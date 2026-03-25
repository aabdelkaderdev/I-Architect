<!-- Source: https://docs.streamlit.io/develop/api-reference/media/st.image -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/image.py#L48 "View st.image source code on GitHub") | |
| --- | --- |
| st.image(image, caption=None, width="content", use\_column\_width=None, clamp=False, channels="RGB", output\_format="auto", \*, use\_container\_width=None, link=None) | |
| Parameters | |
| image (numpy.ndarray, BytesIO, str, Path, or list of these) | The image to display. This can be one of the following:   - A URL (string) for a hosted image. - A path to a local image file. The path can be a str   or Path object. Paths can be absolute or relative to the   working directory (where you execute streamlit run). - An SVG string like <svg xmlns=...</svg>. - A byte array defining an image. This includes monochrome images of   shape (w,h) or (w,h,1), color images of shape (w,h,3), or RGBA   images of shape (w,h,4), where w and h are the image width and   height, respectively. - A list of any of the above. Streamlit displays the list as a   row of images that overflow to additional rows as needed. |
| caption (str or list of str) | Image caption(s). If this is None (default), no caption is displayed. If image is a list of multiple images, caption must be a list of captions (one caption for each image) or None.  Captions can optionally contain GitHub-flavored Markdown. Syntax information can be found at: <https://github.github.com/gfm>.  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives. |
| width ("content", "stretch", or int) | The width of the image element. This can be one of the following:   - "content" (default): The width of the element matches the   width of its content, but doesn't exceed the width of the parent   container. - "stretch": The width of the element matches the width of the   parent container. - An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container.   When using an SVG image without a default width, use "stretch" or an integer. |
| use\_column\_width ("auto", "always", "never", or bool) | *delete* use\_column\_width is deprecated and will be removed in a future release. Please use the width parameter instead.  If "auto", set the image's width to its natural size, but do not exceed the width of the column. If "always" or True, set the image's width to the column width. If "never" or False, set the image's width to its natural size. Note: if set, use\_column\_width takes precedence over the width parameter. |
| clamp (bool) | Whether to clamp image pixel values to a valid range (0-255 per channel). This is only used for byte array images; the parameter is ignored for image URLs and files. If this is False (default) and an image has an out-of-range value, a RuntimeError will be raised. |
| channels ("RGB" or "BGR") | The color format when image is an nd.array. This is ignored for other image types. If this is "RGB" (default), image[:, :, 0] is the red channel, image[:, :, 1] is the green channel, and image[:, :, 2] is the blue channel. For images coming from libraries like OpenCV, you should set this to "BGR" instead. |
| output\_format ("JPEG", "PNG", or "auto") | The output format to use when transferring the image data. If this is "auto" (default), Streamlit identifies the compression type based on the type and format of the image. Photos should use the "JPEG" format for lossy compression while diagrams should use the "PNG" format for lossless compression. |
| use\_container\_width (bool) | *delete* use\_container\_width is deprecated and will be removed in a future release. For use\_container\_width=True, use width="stretch". For use\_container\_width=False, use width="content".  Whether to override width with the width of the parent container. If use\_container\_width is False (default), Streamlit sets the image's width according to width. If use\_container\_width is True, Streamlit sets the width of the image to match the width of the parent container. |
| link (str or None) | The URL to open when a user clicks on the image. This can be an external URL like "https://streamlit.io" or a relative path like "/my\_page". If link is None (default), the image will not include a hyperlink.  This parameter is only supported when displaying a single image. |

#### Example

```
import streamlit as st
st.image("sunrise.jpg", caption="Sunrise by the mountains")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-image.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.audio](/develop/api-reference/media/st.audio)[*arrow\_forward*Next: st.logo](/develop/api-reference/media/st.logo)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI