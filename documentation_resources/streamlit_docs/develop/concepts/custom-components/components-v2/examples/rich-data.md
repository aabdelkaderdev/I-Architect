<!-- Source: https://docs.streamlit.io/develop/concepts/custom-components/components-v2/examples/rich-data -->

This is a component that receives various data types from Python, including an Arrow-serializable dataframe, a JSON-serializable dictionary, and a Base64-encoded image.

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-components-v2-rich-data.streamlit.app/?utm_medium=oembed)

This component demonstrates the following concepts:

- Passing data from Python via the `data` parameter and accessing it in JavaScript
- Automatic dataframe and JSON serialization
- Passing an image as a Base64-encoded string
- Using a placeholder in the component's HTML and dynamically updating it with received data

```
import pandas as pd
import streamlit as st
import base64

# Create sample data
@st.cache_data
def create_sample_df():
    return pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie"],
            "city": ["New York", "London", "Tokyo"],
        }
    )

df = create_sample_df()

# Load an image and convert to b64 string
@st.cache_data
def load_image_as_base64(image_path):
    with open(image_path, "rb") as img_file:
        img_bytes = img_file.read()
    return base64.b64encode(img_bytes).decode("utf-8")

img_base64 = load_image_as_base64("favi.png")

# Serialization is automatically handled by Streamlit components
data_component = st.components.v2.component(
    "data_display",
    html="""<div id="data-container">Loading data...</div>""",
    js="""
    export default function({ data, parentElement }) {
      const container = parentElement.querySelector("#data-container");
      const df = data.df;
      const userInfo = data.user_info;
      const imgBase64 = data.image_base64;
      container.innerHTML = `
        <h4>Dataframe: ${df}</h4>
        <h4>User Info: ${userInfo.name}</h4>
        <img src="data:image/png;base64,${imgBase64}" style="width: 25%;" />
      `;
    }
    """,
)

data_component(
    data={
        "df": df,  # Arrow-serializable dataframe
        "user_info": {"name": "Alice"},  # JSON-serializable data
        "image_base64": img_base64,  # Image as base64 string
    }
)
```

When mounting a component, the `data` parameter passes information from Python to JavaScript. Streamlit automatically serializes the data:

- DataFrames are converted to Apache Arrow format if passed directly to `data` or included as a value in a dictionary.
- Dictionaries, lists, strings, numbers, booleans are JSON-serialized.
- Bytes can be passed directly to `data`, but can't be passed as a value in a dictionary.

The `data` property is available in the component function's argument object:

```
export default function ({ data, parentElement }) {
  // data contains everything passed from Python
  const df = data.df;
  const userInfo = data.user_info;
}
```

DataFrames arrive as Arrow-formatted data on the frontend. In this simple example, they're converted to a string for display. For more sophisticated handling, you can use libraries like Apache Arrow JS to parse and manipulate the data.

When `data` changes between reruns, your component's JavaScript function is called again with the new data. This enables reactive components that update based on Python state. For an example of a bidirectional reactive component, see the [Text input component example](/develop/concepts/custom-components/components-v2/examples/text-input).

[*arrow\_back*Previous: Hello world](/develop/concepts/custom-components/components-v2/examples/hello-world)[*arrow\_forward*Next: Simple button](/develop/concepts/custom-components/components-v2/examples/simple-button)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI