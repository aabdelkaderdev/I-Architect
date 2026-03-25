<!-- Source: https://docs.streamlit.io/develop/concepts/custom-components/components-v2/examples/text-input -->

This is a text input component that demonstrates full bidirectional communication, including programmatic updates from Python.

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-components-v2-text-input.streamlit.app/?utm_medium=oembed)

This component demonstrates the following concepts:

- Mounting a component with a key and reading component state from Session State
- Wrapping a component's raw mounting command to create a user-friendly mounting command
- Programmatic updates from Python via the `data` parameter
- Syncing frontend state without interrupting user input

For easy copying, expand the complete code below. For easier reading, the HTML and JavaScript are shown separately.

Complete single-file code*expand\_more*

```
import streamlit as st

HTML = """
    <label style='padding-right: 1em;' for='txt'>Enter text</label>
    <input id='txt' type='text' />
"""

JS = """
    export default function(component) {
        const { setStateValue, parentElement, data } = component;

        const label = parentElement.querySelector('label');
        label.innerText = data.label;

        const input = parentElement.querySelector('input');
        if (input.value !== data.value) {
            input.value = data.value ?? '';
        };

        input.onkeydown = (e) => {
            if (e.key === 'Enter') {
                setStateValue('value', e.target.value);
            }
        };

        input.onblur = (e) => {
            setStateValue('value', e.target.value);
        };
    }
"""

textbox_component = st.components.v2.component(
    "simple_textbox",
    html=HTML,
    js=JS,
)

def textbox_component_wrapper(
    label, *, default="", key=None, on_change=lambda: None
):
    component_state = st.session_state.get(key, {})
    value = component_state.get("value", default)
    data = {"label": label, "value": value}
    result = textbox_component(
        data=data,
        default={"value": value},
        key=key,
        on_value_change=on_change,
    )
    return result

if st.button("Hello World"):
    st.session_state["my_textbox"]["value"] = "Hello World"
if st.button("Clear text"):
    st.session_state["my_textbox"]["value"] = ""
result = textbox_component_wrapper(
    "Enter something",
    default="I love Streamlit!",
    key="my_textbox",
)

st.write("Result:", result)
st.write("Session state:", st.session_state)
```

```
<label style='padding-right: 1em;' for='txt'>Enter text</label>
<input id='txt' type='text' />
```

```
export default function (component) {
  const { setStateValue, parentElement, data } = component;

  const label = parentElement.querySelector("label");
  label.innerText = data.label;

  const input = parentElement.querySelector("input");
  if (input.value !== data.value) {
    input.value = data.value ?? "";
  }

  input.onkeydown = (e) => {
    if (e.key === "Enter") {
      setStateValue("value", e.target.value);
    }
  };

  input.onblur = (e) => {
    setStateValue("value", e.target.value);
  };
}
```

```
import streamlit as st

textbox_component = st.components.v2.component(
    "simple_textbox",
    html="...",
    js="...",
)

def textbox_component_wrapper(
    label, *, default="", key=None, on_change=lambda: None
):
    component_state = st.session_state.get(key, {})
    value = component_state.get("value", default)
    data = {"label": label, "value": value}
    result = textbox_component(
        data=data,
        default={"value": value},
        key=key,
        on_value_change=on_change,
    )
    return result

if st.button("Hello World"):
    st.session_state["my_textbox"]["value"] = "Hello World"
if st.button("Clear text"):
    st.session_state["my_textbox"]["value"] = ""
result = textbox_component_wrapper(
    "Enter something",
    default="I love Streamlit!",
    key="my_textbox",
)

st.write("Result:", result)
st.write("Session state:", st.session_state)
```

The wrapper function creates a reusable interface for your component:

```
def textbox_component_wrapper(
    label, *, default="", key=None, on_change=lambda: None
):
    # Read current state from Session State
    component_state = st.session_state.get(key, {})
    value = component_state.get("value", default)

    # Pass current value to component
    data = {"label": label, "value": value}
    result = textbox_component(
        data=data,
        default={"value": value},
        key=key,
        on_value_change=on_change,
    )
    return result
```

This pattern:

1. Reads the current value from Session State (falling back to `default`)
2. Passes the value to the component via `data`
3. Returns the result for the caller to use

The JavaScript checks if the value has actually changed before updating:

```
if (input.value !== data.value) {
  input.value = data.value ?? "";
}
```

This prevents the input from being overwritten while the user is typing. Without this check, each rerun would reset the input to the last committed value.

Buttons can modify Session State directly:

```
if st.button("Hello World"):
    st.session_state["my_textbox"]["value"] = "Hello World"
```

On the next rerun, the wrapper reads this new value from Session State and passes it to the component via `data`. The JavaScript then updates the input field.

[*arrow\_back*Previous: Interactive counter](/develop/concepts/custom-components/components-v2/examples/interactive-counter)[*arrow\_forward*Next: Danger button](/develop/concepts/custom-components/components-v2/examples/danger-button)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI