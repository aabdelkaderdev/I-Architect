<!-- Source: https://docs.streamlit.io/develop/api-reference/utilities/st.context -->

Show API reference for

Version v1.55.0*expand\_more*

| Class description[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/runtime/context.py#L145 "View st.context source code on GitHub") | |
| --- | --- |
| st.context() | |
|  |  |
| --- | --- |
| Attributes | |
| [cookies](/develop/api-reference/caching-and-state/st.context#contextcookies) | A read-only, dict-like object containing cookies sent in the initial request. |
| [headers](/develop/api-reference/caching-and-state/st.context#contextheaders) | A read-only, dict-like object containing headers sent in the initial request. |
| [ip\_address](/develop/api-reference/caching-and-state/st.context#contextip_address) | The read-only IP address of the user's connection. |
| [is\_embedded](/develop/api-reference/caching-and-state/st.context#contextis_embedded) | Whether the app is embedded. |
| [locale](/develop/api-reference/caching-and-state/st.context#contextlocale) | The read-only locale of the user's browser. |
| [theme](/develop/api-reference/caching-and-state/st.context#contexttheme) | A read-only, dictionary-like object containing theme information. |
| [timezone](/develop/api-reference/caching-and-state/st.context#contexttimezone) | The read-only timezone of the user's browser. |
| [timezone\_offset](/develop/api-reference/caching-and-state/st.context#contexttimezone_offset) | The read-only timezone offset of the user's browser. |
| [url](/develop/api-reference/caching-and-state/st.context#contexturl) | The read-only URL of the app in the user's browser. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/runtime/context.py#L202 "View st.cookies source code on GitHub") | |
| --- | --- |
| context.cookies | |

#### Examples

**Example 1: Access all available cookies**

Show a dictionary of cookies:

```
import streamlit as st

st.context.cookies
```

**Example 2: Access a specific cookie**

Show the value of a specific cookie:

```
import streamlit as st

st.context.cookies["_ga"]
```

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/runtime/context.py#L156 "View st.headers source code on GitHub") | |
| --- | --- |
| context.headers | |

#### Examples

**Example 1: Access all available headers**

Show a dictionary of headers (with only the last instance of any
repeated key):

```
import streamlit as st

st.context.headers
```

**Example 2: Access a specific header**

Show the value of a specific header (or the last instance if it's
repeated):

```
import streamlit as st

st.context.headers["host"]
```

Show of list of all headers for a given key:

```
import streamlit as st

st.context.headers.get_all("pragma")
```

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/runtime/context.py#L390 "View st.ip_address source code on GitHub") | |
| --- | --- |
| context.ip\_address | |

#### Example

Check if the user has an IPv4 or IPv6 address:

```
import streamlit as st

ip = st.context.ip_address
if ip is None:
    st.write("No IP address. This is expected in local development.")
elif ip.contains(":"):
    st.write("You have an IPv6 address.")
elif ip.contains("."):
    st.write("You have an IPv4 address.")
else:
    st.error("This should not happen.")
```

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/runtime/context.py#L424 "View st.is_embedded source code on GitHub") | |
| --- | --- |
| context.is\_embedded | |

#### Example

Conditionally show content when the app is running in an embedded
context:

```
import streamlit as st

if st.context.is_embedded:
    st.write("You are running the app in an embedded context.")
```

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/runtime/context.py#L331 "View st.locale source code on GitHub") | |
| --- | --- |
| context.locale | |

#### Example

Access the user's locale to display locally:

```
import streamlit as st

if st.context.locale == "fr-FR":
    st.write("Bonjour!")
else:
    st.write("Hello!")
```

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/runtime/context.py#L235 "View st.theme source code on GitHub") | |
| --- | --- |
| context.theme | |
| Parameters | |
| type ("light", "dark") | The theme type inferred from the background color of the app. |

#### Example

Access the theme type of the app:

```
import streamlit as st

st.write(f"The current theme type is {st.context.theme.type}.")
```

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/runtime/context.py#L275 "View st.timezone source code on GitHub") | |
| --- | --- |
| context.timezone | |

#### Example

Access the user's timezone, and format a datetime to display locally:

```
import streamlit as st
from datetime import datetime, timezone
import pytz

tz = st.context.timezone
tz_obj = pytz.timezone(tz)

now = datetime.now(timezone.utc)

f"The user's timezone is {tz}."
f"The UTC time is {now}."
f"The user's local time is {now.astimezone(tz_obj)}"
```

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/runtime/context.py#L304 "View st.timezone_offset source code on GitHub") | |
| --- | --- |
| context.timezone\_offset | |

#### Example

Access the user's timezone offset, and format a datetime to display locally:

```
import streamlit as st
from datetime import datetime, timezone, timedelta

tzoff = st.context.timezone_offset
tz_obj = timezone(-timedelta(minutes=tzoff))

now = datetime.now(timezone.utc)

f"The user's timezone is {tz}."
f"The UTC time is {now}."
f"The user's local time is {now.astimezone(tz_obj)}"
```

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/runtime/context.py#L360 "View st.url source code on GitHub") | |
| --- | --- |
| context.url | |

#### Example

Conditionally show content when you access your app through
localhost:

```
import streamlit as st

if st.context.url.startswith("http://localhost"):
    st.write("You are running the app locally.")
```

[*arrow\_back*Previous: st.session\_state](/develop/api-reference/caching-and-state/st.session_state)[*arrow\_forward*Next: st.query\_params](/develop/api-reference/caching-and-state/st.query_params)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI