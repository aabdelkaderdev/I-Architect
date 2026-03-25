<!-- Source: https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/commands/page_config.py#L110 "View st.set_page_config source code on GitHub") | |
| --- | --- |
| st.set\_page\_config(page\_title=None, page\_icon=None, layout=None, initial\_sidebar\_state=None, menu\_items=None) | |
| Parameters | |
| page\_title (str or None) | The page title, shown in the browser tab. If this is None (default), the page title is inherited from the previous call of st.set\_page\_config. If this is None and no previous call exists, the page title is inferred from the page source.  If a page source is a Python file, its inferred title is derived from the filename. If a page source is a callable object, its inferred title is derived from the callable's name. |
| page\_icon (Anything supported by st.image (except list), str, or None) | The page favicon. If page\_icon is None (default), the page icon is inherited from the previous call of st.set\_page\_config. If this is None and no previous call exists, the favicon is a monochrome Streamlit logo.  In addition to the types supported by [st.image](https://docs.streamlit.io/develop/api-reference/media/st.image) (except list), the following strings are valid:   - A single-character emoji. For example, you can set page\_icon="🦈". - An emoji short code. For example, you can set page\_icon=":shark:".   For a list of all supported codes, see   <https://share.streamlit.io/streamlit/emoji-shortcodes>. - The string literal, "random". You can set page\_icon="random"   to set a random emoji from the supported list above. - An icon from the Material Symbols library (rounded style) in the   format ":material/icon\_name:" where "icon\_name" is the name   of the icon in snake case.  For example, page\_icon=":material/thumb\_up:" will display the   Thumb Up icon. Find additional icons in the [Material Symbols](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded)   font library.   Note  Colors are not supported for Material icons. When you use a Material icon for favicon, it will be black, regardless of browser theme. |
| layout ("centered", "wide", or None) | Layout of the page content. The following layouts are supported:   - None (default): The page layout is inherited from the previous   call of st.set\_page\_config. If no previous call exists, the page   layout is "centered". - "centered": Page elements are constrained to a centered column of   fixed width. - "wide": Page elements use the entire screen width. |
| initial\_sidebar\_state ("auto", "expanded", "collapsed", int, or None) | Initial state of the sidebar. The following states are supported:   - None (default): The sidebar state is inherited from the previous   call of st.set\_page\_config. If no previous call exists, the   sidebar state is "auto". - "auto": The sidebar is hidden on small devices and shown   otherwise. - "expanded": The sidebar is shown initially. - "collapsed": The sidebar is hidden initially. - int: The sidebar will use "auto" behavior but start with the   specified width in pixels. The width must be between 200 and 600   pixels, inclusive.   In most cases, "auto" provides the best user experience across devices of different sizes. |
| menu\_items (dict) | Configure the menu that appears on the top-right side of this app. The keys in this dict denote the menu item to configure. The following keys can have string or None values:   - "Get help": The URL this menu item should point to. - "Report a Bug": The URL this menu item should point to. - "About": A markdown string to show in the About dialog.   A URL may also refer to an email address e.g. mailto:john@example.com.  If you do not include a key, its menu item will be hidden (unless it was set by a previous call to st.set\_page\_config). To remove an item that was specified in a previous call to st.set\_page\_config, set its value to None in the dictionary. |

#### Example

```
import streamlit as st

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
```

[*arrow\_back*Previous: st.set\_option](/develop/api-reference/configuration/st.set_option)[*arrow\_forward*Next: App testing](/develop/api-reference/app-testing)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI