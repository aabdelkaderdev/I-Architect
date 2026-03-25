<!-- Source: https://docs.streamlit.io/develop/concepts/design/timezone-handling -->

In general, working with timezones can be tricky. Your Streamlit app users are not necessarily in the same timezone as the server running your app. It is especially true of public apps, where anyone in the world (in any timezone) can access your app. As such, it is crucial to understand how Streamlit handles timezones, so you can avoid unexpected behavior when displaying `datetime` information.

Streamlit always shows `datetime` information on the frontend with the same information as its corresponding `datetime` instance in the backend. I.e., date or time information does not automatically adjust to the users' timezone. We distinguish between the following two cases:

When you provide a `datetime` instance *without specifying a timezone*, the frontend shows the `datetime` instance without timezone information. For example (this also applies to other widgets like [`st.dataframe`](/develop/api-reference/data/st.dataframe)):

```
import streamlit as st
from datetime import datetime

st.write(datetime(2020, 1, 10, 10, 30))
# Outputs: 2020-01-10 10:30:00
```

Users of the above app always see the output as `2020-01-10 10:30:00`.

When you provide a `datetime` instance *and specify a timezone*, the frontend shows the `datetime` instance in that same timezone. For example (this also applies to other widgets like [`st.dataframe`](/develop/api-reference/data/st.dataframe)):

```
import streamlit as st
from datetime import datetime
import pytz

st.write(datetime(2020, 1, 10, 10, 30, tzinfo=pytz.timezone("EST")))
# Outputs: 2020-01-10 10:30:00-05:00
```

Users of the above app always see the output as `2020-01-10 10:30:00-05:00`.

In both cases, neither the date nor time information automatically adjusts to the users' timezone on the frontend. What users see is identical to the corresponding `datetime` instance in the backend. It is currently not possible to automatically adjust the date or time information to the timezone of the users viewing the app.

The legacy version of the `st.dataframe` has issues with timezones. We do not plan to roll out additional fixes or enhancements for the legacy dataframe. If you need stable timezone support, please consider switching to the arrow serialization by changing the [config setting](/develop/concepts/configuration), *config.dataFrameSerialization = "arrow"*.

[*arrow\_back*Previous: Using custom classes](/develop/concepts/design/custom-classes)[*arrow\_forward*Next: Connections, secrets, and authentication](/develop/concepts/connections)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI