<!-- Source: https://docs.streamlit.io/develop/api-reference/navigation -->

[#### Navigation

Configure the available pages in a multipage app.

```
st.navigation({
    "Your account" : [log_out, settings],
    "Reports" : [overview, usage],
    "Tools" : [search]
})
```](/develop/api-reference/navigation/st.navigation)[#### Page

Define a page in a multipage app.

```
home = st.Page(
    "home.py",
    title="Home",
    icon=":material/home:"
)
```](/develop/api-reference/navigation/st.page)[#### Page link

Display a link to another page in a multipage app.

```
st.page_link("app.py", label="Home", icon="🏠")
st.page_link("pages/profile.py", label="Profile")
```](/develop/api-reference/widgets/st.page_link)[#### Switch page

Programmatically navigates to a specified page.

```
st.switch_page("pages/my_page.py")
```](/develop/api-reference/navigation/st.switch_page)

[*arrow\_back*Previous: Authentication and user info](/develop/api-reference/user)[*arrow\_forward*Next: st.navigation](/develop/api-reference/navigation/st.navigation)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI