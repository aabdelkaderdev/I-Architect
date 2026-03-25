<!-- Source: https://docs.streamlit.io/develop/api-reference/execution-flow/st.dialog -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/dialog_decorator.py#L141 "View st.dialog source code on GitHub") | |
| --- | --- |
| st.dialog(title, \*, width="small", dismissible=True, icon=None, on\_dismiss="ignore") | |
| Parameters | |
| title (str) | The title to display at the top of the modal dialog. It cannot be empty.  The title can optionally contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code, Links, and Images. Images display like icons, with a max height equal to the font height.  Unsupported Markdown elements are unwrapped so only their children (text contents) render. Common block-level Markdown (headings, lists, blockquotes) is automatically escaped and displays as literal text in labels.  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives. |
| width ("small", "medium", "large") | The width of the modal dialog. This can be one of the following:   - "small" (default): The modal dialog will be a maximum of 500   pixels wide. - "medium": The modal dialog will be up to 750 pixels wide. - "large": The modal dialog will be up to 1280 pixels wide. |
| dismissible (bool) | Whether the modal dialog can be dismissed by the user. If this is True (default), the user can dismiss the dialog by clicking outside of it, clicking the "**X**" in its upper-right corner, or pressing ESC on their keyboard. If this is False, the "**X**" in the upper-right corner is hidden and the dialog must be closed programmatically by calling st.rerun() inside the dialog function.  Note  Setting dismissible to False does not guarantee that all interactions in the main app are blocked. Don't rely on dismissible for security-critical checks. |
| icon (str or None) | An optional emoji or icon to display next to the dialog title. If icon is None (default), no icon is displayed. If icon is a string, the following options are valid:   - A single-character emoji. For example, you can set icon="🚨"   or icon="🔥". Emoji short codes are not supported. - An icon from the Material Symbols library (rounded style) in the   format ":material/icon\_name:" where "icon\_name" is the name   of the icon in snake case.  For example, icon=":material/thumb\_up:" will display the   Thumb Up icon. Find additional icons in the [Material Symbols](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded)    font library. - "spinner": Displays a spinner as an icon. |
| on\_dismiss ("ignore", "rerun", or callable) | How the dialog should respond to dismissal events. This can be one of the following:   - "ignore" (default): Streamlit will not rerun the app when the   user dismisses the dialog. - "rerun": Streamlit will rerun the app when the user dismisses   the dialog. - A callable: Streamlit will rerun the app when the user dismisses   the dialog and execute the callable as a callback function   before the rest of the app. |

#### Examples

The following example demonstrates the basic usage of @st.dialog.
In this app, clicking "**A**" or "**B**" will open a modal dialog and prompt you
to enter a reason for your vote. In the modal dialog, click "**Submit**" to record
your vote into Session State and rerun the app. This will close the modal dialog
since the dialog function is not called during the full-script rerun.

```
import streamlit as st

@st.dialog("Cast your vote")
def vote(item):
    st.write(f"Why is {item} your favorite?")
    reason = st.text_input("Because...")
    if st.button("Submit"):
        st.session_state.vote = {"item": item, "reason": reason}
        st.rerun()

if "vote" not in st.session_state:
    st.write("Vote for your favorite")
    if st.button("A"):
        vote("A")
    if st.button("B"):
        vote("B")
else:
    f"You voted for {st.session_state.vote['item']} because {st.session_state.vote['reason']}"
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-modal-dialog.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: Execution flow](/develop/api-reference/execution-flow)[*arrow\_forward*Next: st.form](/develop/api-reference/execution-flow/st.form)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI