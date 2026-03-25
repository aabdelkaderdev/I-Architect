<!-- Source: https://docs.streamlit.io/develop/api-reference/user -->

Streamlit provides native support for user authentication so you can personalize your apps. You can also directly read headers and cookies.

[#### Log in a user

`st.login()` starts an authentication flow with an identity provider.

```
st.login()
```](/develop/api-reference/user/st.login)[#### Log out a user

`st.logout()` removes a user's identity information.

```
st.logout()
```](/develop/api-reference/user/st.logout)[#### User info

`st.user` returns information about a logged-in user.

```
if st.user.is_logged_in:
  st.write(f"Welcome back, {st.user.name}!")
```](/develop/api-reference/user/st.user)

[*arrow\_back*Previous: Third-party components](https://streamlit.io/components)[*arrow\_forward*Next: st.login](/develop/api-reference/user/st.login)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI