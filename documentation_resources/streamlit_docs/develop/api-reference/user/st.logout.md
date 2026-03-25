<!-- Source: https://docs.streamlit.io/develop/api-reference/user/st.logout -->

Show API reference for

Version v1.55.0*expand\_more*

Learn more in [User authentication and information](/develop/concepts/connections/authentication).

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/user_info.py#L309 "View st.logout source code on GitHub") | |
| --- | --- |
| st.logout() | |

#### Example

.streamlit/secrets.toml:

```
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "xxx"
client_id = "xxx"
client_secret = "xxx"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"  # fmt: skip
```

Your app code:

```
import streamlit as st

if not st.user.is_logged_in:
    if st.button("Log in"):
        st.login()
else:
    if st.button("Log out"):
        st.logout()
    st.write(f"Hello, {st.user.name}!")
```

[*arrow\_back*Previous: st.login](/develop/api-reference/user/st.login)[*arrow\_forward*Next: st.user](/develop/api-reference/user/st.user)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI