<!-- Source: https://docs.streamlit.io/develop/api-reference/user/st.user -->

Show API reference for

Version v1.55.0*expand\_more*

| Class description[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/user_info.py#L527 "View st.user source code on GitHub") | |
| --- | --- |
| st.user() | |
|  |  |
| --- | --- |
| Methods | |
| [to\_dict](/develop/api-reference/user/st.user#userto_dict)() | Get user info as a dictionary. |
| Attributes | |
| is\_logged\_in (bool) | Whether a user is logged in. For a locally running app, this attribute is only available when authentication (st.login()) is configured in secrets.toml. Otherwise, it does not exist. |
| tokens (TokensProxy) | A read-only, dict-like object for accessing exposed tokens from the identity provider. |

#### Examples

**Example 1: Google's identity token**

If you configure a basic Google OIDC connection as shown in Example 1 of
st.login(), the following data is available in
st.user. Streamlit adds the is\_logged\_in attribute.
Additional attributes may be available depending on the configuration of
the user's Google account. For more information about Google's identity
tokens, see [Obtain user information from the ID token](https://developers.google.com/identity/openid-connect/openid-connect#obtainuserinfo)
in Google's docs.

```
import streamlit as st

if st.user.is_logged_in:
    st.write(st.user)
```

Displayed data when a user is logged in:

```
{
    "is_logged_in":true
    "iss":"https://accounts.google.com"
    "azp":"{client_id}.apps.googleusercontent.com"
    "aud":"{client_id}.apps.googleusercontent.com"
    "sub":"{unique_user_id}"
    "email":"{user}@gmail.com"
    "email_verified":true
    "at_hash":"{access_token_hash}"
    "nonce":"{nonce_string}"
    "name":"{full_name}"
    "picture":"https://lh3.googleusercontent.com/a/{content_path}"
    "given_name":"{given_name}"
    "family_name":"{family_name}"
    "iat":{issued_time}
    "exp":{expiration_time}
    "tokens":{}
}
```

**Example 2: Microsoft's identity token**

If you configure a basic Microsoft OIDC connection as shown in Example 2 of
st.login(), the following data is available in
st.user. For more information about Microsoft's identity
tokens, see [ID token claims reference](https://learn.microsoft.com/en-us/entra/identity-platform/id-token-claims-reference)
in Microsoft's docs.

```
import streamlit as st

if st.user.is_logged_in:
    st.write(st.user)
```

Displayed data when a user is logged in:

```
{
    "is_logged_in":true
    "ver":"2.0"
    "iss":"https://login.microsoftonline.com/{tenant_id}/v2.0"
    "sub":"{application_user_id}"
    "aud":"{application_id}"
    "exp":{expiration_time}
    "iat":{issued_time}
    "nbf":{start_time}
    "name":"{full_name}"
    "preferred_username":"{username}"
    "oid":"{user_GUID}"
    "email":"{email}"
    "tid":"{tenant_id}"
    "nonce":"{nonce_string}"
    "aio":"{opaque_string}"
    "tokens":{}
}
```

|  |  |
| --- | --- |
| Attributes | |
| id (str) | The identity token. This is only available if "id" is in expose\_tokens. |
| access (str) | The access token. This is only available if "access" is in expose\_tokens. |

#### Examples

**Example 1: Expose the ID token**

To expose only the identity token, add expose\_tokens to your
authentication configuration. This example uses an unnamed default provider.

```
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "xxx"
client_id = "xxx"
client_secret = "xxx"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
expose_tokens = "id"
```

```
import streamlit as st

if st.user.is_logged_in:
    id_token = st.user.tokens["id"]
    # Use the token for API verification
```

**Example 2: Expose both ID and access tokens**

You can use a list to expose multiple tokens. If you use one or more named
identity providers, the same tokens must be exposed for all providers in
the shared [auth] section.

```
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "xxx"
expose_tokens = ["id", "access"]

[auth.google]
client_id = "xxx"
client_secret = "xxx"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"

[auth.microsoft]
client_id = "xxx"
client_secret = "xxx"
server_metadata_url = "https://login.microsoftonline.com/{tenant}/v2.0/.well-known/openid-configuration"
```

```
import streamlit as st

if st.user.is_logged_in:
    id_token = st.user.tokens["id"]
    access_token = st.user.tokens["access"]
    # Use the tokens for API verification
```

Starting from Streamlit version 1.42.0, you can't use `st.user` to retrieve a user's Community Cloud account email. To access user information, you must set up an identity provider and configure authentication (`[auth]`) in your app's secrets. Remember to update your identity provider's configuration and your app's secrets to allow your new domain. A list of [IP addresses](/deploy/streamlit-community-cloud/status#ip-addresses) used by Community Cloud is available if needed. An authentication-configured app counts as your single allowed private app.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/user_info.py#L677 "View st.to_dict source code on GitHub") | |
| --- | --- |
| st.user.to\_dict() | |
|  |  |
| --- | --- |
| Returns | |
| (Dict[str,str]) | A dictionary of the current user's information. |

[*arrow\_back*Previous: st.logout](/develop/api-reference/user/st.logout)[*arrow\_forward*Next: Navigation and pages](/develop/api-reference/navigation)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI