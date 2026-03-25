<!-- Source: https://docs.streamlit.io/knowledge-base/using-streamlit/widget-updating-session-state -->

You are using [session state](/develop/api-reference/caching-and-state/st.session_state) to store page interactions in your app. When users interact with a widget in your app (e.g., click a button), you expect your app to update its widget states and reflect the new values. However, you notice that it doesn't. Instead, users have to interact with the widget twice (e.g., click a button twice) for the app to show the correct values. What do you do now? 🤔 Let's walk through the solution in the section below.

When using session state to update widgets or values in your script, you need to use the unique key you assigned to the widget, **not** the variable that you assigned your widget to. In the example code block below, the unique *key* assigned to the slider widget is `slider`, and the *variable* the widget is assigned to is `slide_val`.

Let's see this in an example. Say you want a user to click a button that resets a slider.

To have the slider's value update on the button click, you need to use a [callback function](/develop/api-reference/caching-and-state/st.session_state#use-callbacks-to-update-session-state) with the `on_click` parameter of [`st.button`](/develop/api-reference/widgets/st.button):

```
# the callback function for the button will add 1 to the
# slider value up to 10
def plus_one():
    if st.session_state["slider"] < 10:
        st.session_state.slider += 1
    else:
        pass
    return

# when creating the button, assign the name of your callback
# function to the on_click parameter
add_one = st.button("Add one to the slider", on_click=plus_one, key="add_one")

# create the slider
slide_val = st.slider("Pick a number", 0, 10, key="slider")
```

- [Caching Sqlite DB connection resulting in glitchy rendering of the page](https://discuss.streamlit.io/t/caching-sqlite-db-connection-resulting-in-glitchy-rendering-of-the-page/19017)
- [Select all checkbox that is linked to selectbox of options](https://discuss.streamlit.io/t/select-all-checkbox-that-is-linked-to-selectbox-of-options/18521)

[*arrow\_back*Previous: Where does st.file\_uploader store uploaded files and when do they get deleted?](/knowledge-base/using-streamlit/where-file-uploader-store-when-deleted)[*arrow\_forward*Next: Why does Streamlit restrict nested st.columns?](/knowledge-base/using-streamlit/why-streamlit-restrict-nested-columns)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI