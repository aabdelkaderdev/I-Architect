<!-- Source: https://docs.streamlit.io/develop/api-reference/write-magic/st.write -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/elements/write.py#L274 "View st.write source code on GitHub") | |
| --- | --- |
| st.write(\*args, unsafe\_allow\_html=False) | |
| Parameters | |
| \*args (any) | One or many objects to display in the app.   Each type of argument is handled as follows:     | Type | Handling | | --- | --- | | str | Uses st.markdown(). | | dataframe-like, dict, or list | Uses st.dataframe(). | | Exception | Uses st.exception(). | | function, module, or class | Uses st.help(). | | DeltaGenerator | Uses st.help(). | | Altair chart | Uses st.altair\_chart(). | | Bokeh figure | Uses st.bokeh\_chart(). | | Graphviz graph | Uses st.graphviz\_chart(). | | Keras model | Converts model and uses st.graphviz\_chart(). | | Matplotlib figure | Uses st.pyplot(). | | Plotly figure | Uses st.plotly\_chart(). | | PIL.Image | Uses st.image(). | | generator or stream (like openai.Stream) | Uses st.write\_stream(). | | SymPy expression | Uses st.latex(). | | An object with .\_repr\_html() | Uses st.html(). | | Database cursor | Displays DB API 2.0 cursor results in a table. | | Any | Displays str(arg) as inline code. | |
| unsafe\_allow\_html (bool) | Whether to render HTML within \*args. This only applies to strings or objects falling back on \_repr\_html\_(). If this is False (default), any HTML tags found in body will be escaped and therefore treated as raw text. If this is True, any HTML expressions within body will be rendered.  Adding custom HTML to your app impacts safety, styling, and maintainability.  Note  If you only want to insert HTML or CSS without Markdown text, we recommend using st.html instead. |
|  |  |
| --- | --- |
| Returns | |
| (None) | No description |

#### Examples

Its basic use case is to draw Markdown-formatted text, whenever the
input is a string:

```
import streamlit as st

st.write("Hello, *World!* :sunglasses:")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-write1.streamlit.app//?utm_medium=oembed&)

As mentioned earlier, st.write() also accepts other data formats, such as
numbers, data frames, styled data frames, and assorted objects:

```
import streamlit as st
import pandas as pd

st.write(1234)
st.write(
    pd.DataFrame(
        {
            "first column": [1, 2, 3, 4],
            "second column": [10, 20, 30, 40],
        }
    )
)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-write2.streamlit.app//?utm_medium=oembed&)

Finally, you can pass in multiple arguments to do things like:

```
import streamlit as st

st.write("1 + 1 = ", 2)
st.write("Below is a DataFrame:", data_frame, "Above is a dataframe.")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-write3.streamlit.app//?utm_medium=oembed&)

Oh, one more thing: st.write accepts chart objects too! For example:

```
import altair as alt
import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng

df = pd.DataFrame(rng(0).standard_normal((200, 3)), columns=["a", "b", "c"])
chart = (
    alt.Chart(df)
    .mark_circle()
    .encode(x="a", y="b", size="c", color="c", tooltip=["a", "b", "c"])
)

st.write(chart)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-vega-lite-chart.streamlit.app//?utm_medium=oembed&)

Learn what the [`st.write`](/develop/api-reference/write-magic/st.write) and [magic](/develop/api-reference/write-magic/magic) commands are and how to use them.

[*arrow\_back*Previous: Write and magic](/develop/api-reference/write-magic)[*arrow\_forward*Next: st.write\_stream](/develop/api-reference/write-magic/st.write_stream)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI