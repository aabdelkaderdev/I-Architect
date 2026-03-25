<!-- Source: https://docs.streamlit.io/develop/api-reference/navigation/st.page -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/navigation/page.py#L32 "View st.Page source code on GitHub") | |
| --- | --- |
| st.Page(page, \*, title=None, icon=None, url\_path=None, default=False, visibility="visible") | |
| Parameters | |
| page (str, Path, or callable) | The page source as a Callable or path to a Python file. If the page source is defined by a Python file, the path can be a string or pathlib.Path object. Paths can be absolute or relative to the entrypoint file. If the page source is defined by a Callable, the Callable can't accept arguments. |
| title (str or None) | The title of the page. If this is None (default), the page title (in the browser tab) and label (in the navigation menu) will be inferred from the filename or callable name in page. For more information, see [Overview of multipage apps](https://docs.streamlit.io/st.page.automatic-page-labels).  The title supports GitHub-flavored Markdown of the following types: Bold, Italics, Strikethrough, Inline Code, and Images. Images display like icons, with a max height equal to the font height.  Unsupported Markdown elements are unwrapped so only their children (text contents) render. Common block-level Markdown (headings, lists, blockquotes) is automatically escaped and displays as literal text in labels.  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives. |
| icon (str or None) | An optional emoji or icon to display next to the page title and label. If icon is None (default), no icon is displayed next to the page label in the navigation menu, and a Streamlit icon is displayed next to the title (in the browser tab). If icon is a string, the following options are valid:   - A single-character emoji. For example, you can set icon="🚨"  or icon="🔥". Emoji short codes are not supported. - An icon from the Material Symbols library (rounded style) in the  format ":material/icon\_name:" where "icon\_name" is the name   of the icon in snake case.  For example, icon=":material/thumb\_up:" will display the   Thumb Up icon. Find additional icons in the [Material Symbols](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded)   font library. - "spinner": Displays a spinner as an icon. In this case, the   spinner only displays next to the page label in the navigation menu.   The spinner isn't used as the page favicon next to the title in the   browser tab. The favicon is the default Streamlit icon unless   otherwise specified with the page\_icon parameter of   st.set\_page\_config. |
| url\_path (str or None) | The page's URL pathname, which is the path relative to the app's root URL. If this is None (default), the URL pathname will be inferred from the filename or callable name in page. For more information, see [Overview of multipage apps](https://docs.streamlit.io/st.page.automatic-page-urls).  The default page will have a pathname of "", indicating the root URL of the app. If you set default=True, url\_path is ignored. url\_path can't include forward slashes; paths can't include subdirectories. |
| default (bool) | Whether this page is the default page to be shown when the app is loaded. If default is False (default), the page will have a nonempty URL pathname. However, if no default page is passed to st.navigation and this is the first page, this page will become the default page. If default is True, then the page will have an empty pathname and url\_path will be ignored. |
| visibility ("visible" or "hidden") | Whether the page is shown in the navigation menu. If this is "visible" (default), the page appears in the navigation menu. If this is "hidden", the page is excluded from the navigation menu but remains accessible via direct URL, st.page\_link, or st.switch\_page.  Note  Navigating to a page by URL starts a new session. For a hidden page to be accessible by URL, it must be passed to st.navigation during the new session's initial script run. |
|  |  |
| --- | --- |
| Returns | |
| (StreamlitPage) | The page object associated to the given script. |

#### Example

```
import streamlit as st

def page2():
    st.title("Second page")

pg = st.navigation([
    st.Page("page1.py", title="First page", icon="🔥"),
    st.Page(page2, title="Second page", icon=":material/favorite:"),
])
pg.run()
```

| Class description[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/navigation/page.py#L173 "View st.StreamlitPage source code on GitHub") | |
| --- | --- |
| StreamlitPage(page, \*, title=None, icon=None, url\_path=None, default=False, visibility="visible") | |
|  |  |
| --- | --- |
| Methods | |
| [run](/develop/api-reference/navigation/st.page#stpagerun)() | Execute the page. |
| Attributes | |
| icon (str) | The icon of the page.  If no icon was declared in st.Page, this property returns "". |
| title (str) | The title of the page.  Unless declared otherwise in st.Page, the page title is inferred from the filename or callable name. For more information, see [Overview of multipage apps](https://docs.streamlit.io/st.page.automatic-page-labels).  The title supports GitHub-flavored Markdown as described in st.Page. |
| url\_path (str) | The page's URL pathname, which is the path relative to the app's root URL.  Unless declared otherwise in st.Page, the URL pathname is inferred from the filename or callable name. For more information, see [Overview of multipage apps](https://docs.streamlit.io/st.page.automatic-page-urls).  The default page will always have a url\_path of "" to indicate the root URL (e.g. homepage). |
| visibility (Literal["visible", "hidden"]) | Whether the page is shown in the navigation menu. If this is "visible" (default), the page appears in the navigation menu. If this is "hidden", the page is excluded from the navigation menu but remains accessible via direct URL, st.page\_link, or st.switch\_page.  Note  Navigating to a page by URL starts a new session. For a hidden page to be accessible by URL, it must be passed to st.navigation during the new session's initial script run. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/navigation/page.py#L354 "View st.run source code on GitHub") | |
| --- | --- |
| StreamlitPage.run() | |

[*arrow\_back*Previous: st.navigation](/develop/api-reference/navigation/st.navigation)[*arrow\_forward*Next: st.page\_link](https://docs.streamlit.io/develop/api-reference/widgets/st.page_link)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI