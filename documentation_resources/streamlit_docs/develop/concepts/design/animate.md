<!-- Source: https://docs.streamlit.io/develop/concepts/design/animate -->

Most Streamlit commands draw something on the screen, and most commands also return an object. What that object is — and what you can do with it — depends on the type of command. Understanding this is the key to updating your app's display in place without triggering a full rerun.

Streamlit commands fall into three categories based on what they return:

Commands like `st.markdown`, `st.image`, `st.dataframe`, and `st.line_chart` draw a single visible element. They return an **element object**, an object you can use to replace or clear that element later:

```
import streamlit as st

el = st.text("Loading...")
# Later, replace the text with something else:
el.write("Done!")
```

You can call `.empty()` on any element object to clear it from the screen:

```
import streamlit as st

el = st.text("Temporary message")
el.empty()
```

Commands like `st.container`, `st.columns`, `st.tabs`, and `st.empty` create regions that hold other elements. They return a **container object** that you can write into using method calls or context managers:

```
import streamlit as st

c = st.container()
c.write("Written via method call")

with c:
    st.write("Written via context manager")
```

`st.empty` is a special container that holds only one element at a time. Each write to an `st.empty` object replaces the previous content. This makes it the primary tool for in-place updates. For more on containers, see [Using layouts and containers](/develop/concepts/design/layouts-and-containers).

Commands like `st.slider`, `st.selectbox`, `st.button`, and `st.text_input` are widgets. They return a **Python value** like `int`, `str`, or `bool` instead of an abstract Streamlit object. You interact with widget state through `st.session_state` and callbacks, not by calling methods on their returned values:

```
import streamlit as st

val = st.slider("Pick a number", 0, 100)
st.write(f"You picked {val}")
```

For details on how widgets manage state and identity, see [Widget behavior](/develop/concepts/architecture/widget-behavior).

Some elements can switch into **widget mode** when configured with interactive parameters. In widget mode, the element either returns its state directly, or its usual element object has state attributes. Elements in widget mode follow widget rules with respect to keys, callbacks, and Session State.

For example, `st.dataframe` normally returns an element object. However, when you set `on_select="rerun"`, it returns a selection dictionary instead:

```
import streamlit as st
import pandas as pd

df = pd.DataFrame({"Name": ["Alice", "Bob"], "Score": [85, 92]})

# Default mode: returns an element object
el = st.dataframe(df)

# Widget mode: returns a selection dictionary
selection = st.dataframe(df, on_select="rerun", key="my_table")
st.write(selection)
```

Similarly, `st.tabs`, `st.expander`, and `st.popover` become widget-like when you set `on_change`. They still return container objects, but they also track state, which is available as attributes on the container objects. See [Dynamic containers](/develop/concepts/design/layouts-and-containers#dynamic-containers) for details.

The most common pattern for in-place updates is using `st.empty`:

```
import streamlit as st
import time

placeholder = st.empty()

for i in range(5):
    placeholder.write(f"Iteration {i}")
    time.sleep(0.5)

placeholder.empty()
```

To replace a group of elements, nest `st.container` inside `st.empty`:

```
import streamlit as st
import time

placeholder = st.empty()

with placeholder.container():
    st.write("First set of content")
    st.button("A button")

time.sleep(2)

with placeholder:
    st.write("Replacement content")
```

Any element (not just `st.empty`) supports replacement and clearing. This works because every non-widget Streamlit command returns an element object for the position it occupies in the app:

```
import streamlit as st

el = st.text("Loading...")
# Later, replace the text with something else:
el.write("Done!")
```

Some elements have specialized update methods beyond replacement:

Update a progress bar by calling `.progress()` on the returned object. Clear it with `.empty()`:

```
import streamlit as st
import time

bar = st.progress(0, text="Working...")

for i in range(100):
    time.sleep(0.02)
    bar.progress(i + 1, text=f"Working... {i + 1}%")

bar.empty()
```

Update a status container's label, state, and expanded state with `.update()`:

```
import streamlit as st
import time

with st.status("Downloading data...", expanded=True) as status:
    st.write("Searching for data...")
    time.sleep(1)
    st.write("Downloading...")
    time.sleep(1)
    status.update(label="Download complete!", state="complete", expanded=False)
```

Update a toast notification in place by calling `.toast()` on the returned object:

```
import streamlit as st
import time

msg = st.toast("Starting process...")
time.sleep(1)
msg.toast("Almost there...")
time.sleep(1)
msg.toast("Done!", icon="✅")
```

`st.dataframe`, `st.table`, and basic chart elements like `st.line_chart` support an `.add_rows()` method that appends data to the element without replacing it. This is useful for streaming data or building up a chart incrementally:

```
import streamlit as st
import pandas as pd
import numpy as np
import time

df = pd.DataFrame(np.random.randn(15, 3), columns=["A", "B", "C"])
chart = st.line_chart(df)

for tick in range(10):
    time.sleep(0.5)
    new_row = pd.DataFrame(np.random.randn(1, 3), columns=["A", "B", "C"])
    chart.add_rows(new_row)

st.button("Regenerate")
```

The Streamlit team is evaluating the future of `.add_rows()`. If you use this method, please share your feedback in the [community discussion](https://github.com/streamlit/streamlit/issues/13063).

[*arrow\_back*Previous: Using layouts and containers](/develop/concepts/design/layouts-and-containers)[*arrow\_forward*Next: Button behavior and examples](/develop/concepts/design/buttons)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI