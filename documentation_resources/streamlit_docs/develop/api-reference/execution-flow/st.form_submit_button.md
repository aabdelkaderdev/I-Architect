<!-- Source: https://docs.streamlit.io/develop/api-reference/execution-flow/st.form_submit_button -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/form.py#L246 "View st.form_submit_button source code on GitHub") | |
| --- | --- |
| st.form\_submit\_button(label="Submit", help=None, on\_click=None, args=None, kwargs=None, \*, key=None, type="secondary", icon=None, icon\_position="left", disabled=False, use\_container\_width=None, width="content", shortcut=None) | |
| Parameters | |
| label (str) | A short label explaining to the user what this button is for. This defaults to "Submit". The label can optionally contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code, Links, and Images. Images display like icons, with a max height equal to the font height.  Unsupported Markdown elements are unwrapped so only their children (text contents) render. Common block-level Markdown (headings, lists, blockquotes) is automatically escaped and displays as literal text in labels.  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives. |
| help (str or None) | A tooltip that gets displayed when the button is hovered over. If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| on\_click (callable) | An optional callback invoked when this button is clicked. |
| args (list or tuple) | An optional list or tuple of args to pass to the callback. |
| kwargs (dict) | An optional dict of kwargs to pass to the callback. |
| key (str, int, or None) | An optional string or integer to use as the unique key for the widget. If this is None (default), a key will be generated for the widget based on the values of the other parameters. No two widgets may have the same key. Assigning a key stabilizes the widget's identity and preserves its state across reruns even when other parameters change.  A key lets you access the widget's value via st.session\_state[key] (read-only). For more details, see [Widget behavior](https://docs.streamlit.io/develop/concepts/architecture/widget-behavior).  Additionally, if key is provided, it will be used as a CSS class name prefixed with st-key-. |
| type ("primary", "secondary", or "tertiary") | An optional string that specifies the button type. This can be one of the following:   - "primary": The button's background is the app's primary color   for additional emphasis. - "secondary" (default): The button's background coordinates   with the app's background color for normal emphasis. - "tertiary": The button is plain text without a border or   background for subtlety. |
| icon (str or None) | An optional emoji or icon to display next to the button label. If icon is None (default), no icon is displayed. If icon is a string, the following options are valid:   - A single-character emoji. For example, you can set icon="🚨"   or icon="🔥". Emoji short codes are not supported. - An icon from the Material Symbols library (rounded style) in the   format ":material/icon\_name:" where "icon\_name" is the name   of the icon in snake case.  For example, icon=":material/thumb\_up:" will display the   Thumb Up icon. Find additional icons in the [Material Symbols](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded)   font library. - "spinner": Displays a spinner as an icon. |
| icon\_position ("left" or "right") | The position of the icon relative to the button label. This defaults to "left". |
| disabled (bool) | Whether to disable the button. If this is False (default), the user can interact with the button. If this is True, the button is grayed-out and can't be clicked.  If the first st.form\_submit\_button in the form is disabled, the form will override submission behavior with enter\_to\_submit=False. |
| use\_container\_width (bool) | *delete* use\_container\_width is deprecated and will be removed in a future release. For use\_container\_width=True, use width="stretch". For use\_container\_width=False, use width="content".  Whether to expand the button's width to fill its parent container. If use\_container\_width is False (default), Streamlit sizes the button to fit its contents. If use\_container\_width is True, the width of the button matches its parent container.  In both cases, if the contents of the button are wider than the parent container, the contents will line wrap. |
| width ("content", "stretch", or int) | The width of the button. This can be one of the following:   - "content" (default): The width of the button matches the   width of its content, but doesn't exceed the width of the parent   container. - "stretch": The width of the button matches the width of the   parent container. - An integer specifying the width in pixels: The button has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the button matches the width   of the parent container. |
| shortcut (str or None) | An optional keyboard shortcut that triggers the button. This can be one of the following strings:   - A single alphanumeric key like "K" or "4". - A function key like "F11". - A special key like "Enter", "Esc", or "Tab". - Any of the above combined with modifiers. For example, you can use   "Ctrl+K" or "Cmd+Shift+O".   Important  The keys "C" and "R" are reserved and can't be used, even with modifiers. Punctuation keys like "." and "," aren't currently supported.  For a list of supported keys and modifiers, see the documentation for [st.button](https://docs.streamlit.io/develop/api-reference/widgets/st.button). |
|  |  |
| --- | --- |
| Returns | |
| (bool) | True if the button was clicked. |

[*arrow\_back*Previous: st.form](/develop/api-reference/execution-flow/st.form)[*arrow\_forward*Next: st.fragment](/develop/api-reference/execution-flow/st.fragment)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI