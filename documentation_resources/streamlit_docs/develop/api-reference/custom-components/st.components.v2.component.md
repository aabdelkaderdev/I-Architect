<!-- Source: https://docs.streamlit.io/develop/api-reference/custom-components/st.components.v2.component -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/components/v2/__init__.py#L207 "View st.component source code on GitHub") | |
| --- | --- |
| st.components.v2.component(name, \*, html=None, css=None, js=None, isolate\_styles=True) | |
| Parameters | |
| name (str) | A short, descriptive identifier for the component. This is used internally by Streamlit to manage instances of the component.  Component names must be unique across an app. The names of imported components are prefixed by their module name to avoid collisions.  If you register multiple components with the same name, a warning is logged and the last-registered component is used. Because this can lead to unexpected behavior, ensure that component names are unique. If you intend to have multiple instances of a component in one app, avoid wrapping a component definition together with its mounting command so you don't re-register your component with each instance. |
| html (str or None) | Inline HTML markup for the component root. This can be one of the following strings:   - Raw HTML. This doesn't require any <html>, <head>, or   <body> tags; just provide the inner HTML. - A path or glob to an HTML file, relative to the component's   asset directory.   If any HTML depends on data passed at mount time, use a placeholder element and populate it via JavaScript. Alternatively, you can append a new element to the parent. For more information, see Example 2. |
| css (str or None) | Inline CSS. This can be one of the following strings:   - Raw CSS (without a <style> block). - A path or glob to a CSS file, relative to the component's   asset directory. |
| js (str or None) | Inline JavaScript. This can be one of the following strings:   - Raw JavaScript (without a <script> block). - A path or glob to a JS file, relative to the component's   asset directory. |
| isolate\_styles (bool) | Whether to sandbox the component styles in a shadow root. If this is True (default), the component's HTML is mounted inside a shadow DOM and, in your component's JavaScript, parentElement returns a ShadowRoot. If this is False, the component's HTML is mounted directly into the app's DOM tree, and parentElement returns a regular HTMLElement. |
|  |  |
| --- | --- |
| Returns | |
| (ComponentRenderer) | The component's mounting command.  This callable accepts the component parameters like key and data and returns a BidiComponentResult object with the component's state. The mounting command can be included in a user-friendly wrapper function to provide a simpler API. A mounting command can be called multiple times in an app to create multiple instances of the component. |

#### Examples

**Example 1: Create a JavaScript-only component that captures link clicks**

You can create a simple component that allows inline links to communicate
with Python. Normally, clicking links in a Streamlit app would start a new
session. This component captures link clicks and sends them to Python as
trigger values.

```
import streamlit as st

JS = """
export default function(component) {
    const { setTriggerValue } = component;
    const links = document.querySelectorAll('a[href="#"]');

    links.forEach((link) => {
        link.onclick = (e) => {
            setTriggerValue('clicked', link.innerHTML);
        };
    });
}
"""

my_component = st.components.v2.component(
    "inline_links",
    js=JS,
)

result = my_component(on_clicked_change=lambda: None)

st.markdown(
    "Components aren't [sandboxed](#), so you can write JS that [interacts](#) with the main [document](#)."
)

if result.clicked:
    st.write(f"You clicked {result.clicked}!")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-components-markdown-links.streamlit.app//?utm_medium=oembed&)

**Example 2: Display a paragraph with custom inline links**

If you want to dynamically pass custom data from inline links, you can pass
HTML to the data parameter of the component's mount command. When a
link is clicked, the component sets a trigger value from the link's
data-link HTML attribute.

Warning

If you directly modify the inner HTML of the parent element, you will
overwrite the HTML and CSS passed to the component. Instead, create a
new child element and set its inner HTML. You can create the
placeholder dynamically in JavaScript or include it in the html
parameter.

```
import streamlit as st

CSS = """
a {
    color: var(--st-link-color);
}
"""

JS = """
export default function(component) {
    const { data, setTriggerValue, parentElement } = component;
    const newElement = document.createElement('div');
    parentElement.appendChild(newElement);
    newElement.innerHTML = data;

    const links = newElement.querySelectorAll('a');

    links.forEach((link) => {
        link.onclick = (e) => {
            setTriggerValue('clicked', link.getAttribute('data-link'));
        };
    });
}
"""

my_component = st.components.v2.component(
    "inline_links",
    css=CSS,
    js=JS,
)

paragraph_html = """
<p>This is an example paragraph with inline links. To see the response in
Python, click on the <a href="#" data-link="link_1">first link</a> or
<a href="#" data-link="link_2">second link</a>.</p>
"""

result = my_component(data=paragraph_html, on_clicked_change=lambda: None)
if result.clicked == "link_1":
    st.write("You clicked the first link!")
elif result.clicked == "link_2":
    st.write("You clicked the second link!")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-components-custom-anchors.streamlit.app//?utm_medium=oembed&)

**Example 3: Display an interactive SVG image**

You can create a component that displays an SVG image with clickable
shapes. When a shape is clicked, the component sends the shape type to
Python as a trigger value.

```
import streamlit as st

HTML = """
<p>Click on the triangle, square, or circle to interact with the shapes:</p>

<svg width="400" height="300">
    <polygon points="100,50 50,150 150,150" data-shape="triangle"></polygon>
    <rect x="200" y="75" width="100" height="100" data-shape="square"></rect>
    <circle cx="125" cy="225" r="40" data-shape="circle"></circle>
</svg>
"""

JS = """
export default function(component) {
    const { setTriggerValue, parentElement } = component;
    const shapes = parentElement.querySelectorAll('[data-shape]');

    shapes.forEach((shape) => {
        shape.onclick = (e) => {
            setTriggerValue('clicked', shape.getAttribute('data-shape'));
        };
    });
}
"""

CSS = """
polygon, rect, circle {
    stroke: var(--st-primary-color);
    stroke-width: 2;
    fill: transparent;
    cursor: pointer;
}
polygon:hover, rect:hover, circle:hover {
    fill: var(--st-secondary-background-color);
}
"""

my_component = st.components.v2.component(
    "clickable_svg",
    html=HTML,
    css=CSS,
    js=JS,
)

result = my_component(on_clicked_change=lambda: None)
result
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-components-interactive-svg.streamlit.app//?utm_medium=oembed&)

**Example 4: Clean up your component's resources**

You can use the return value of the component's JavaScript function to
clean up any resources when the component is unmounted. For example, you
can disconnect a MutationObserver that was monitoring changes in the DOM.

```
import streamlit as st

JS = """
export default function(component) {
    const { setStateValue, parentElement } = component;
    const sidebar = document.querySelector('section.stSidebar');
    const initialState = sidebar.getAttribute('aria-expanded') === 'true';

    // Create observer to watch for aria-expanded attribute changes
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.type === 'attributes' && mutation.attributeName === 'aria-expanded') {
                const newIsExpanded = sidebar.getAttribute('aria-expanded') === 'true';
                setStateValue('expanded', newIsExpanded);
            }
        });
    });

    // Start observing
    observer.observe(sidebar, {
        attributes: true,
        attributeFilter: ['aria-expanded']
    });

    // Set initial state
    setStateValue('expanded', initialState);

    // Cleanup function to remove the observer
    return () => {
        observer.disconnect();
    };

};
"""

my_component = st.components.v2.component(
    "sidebar_expansion_detector",
    js=JS,
)

st.sidebar.write("Sidebar content")
result = my_component(on_expanded_change=lambda: None)
result
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-components-cleanup-function.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: Custom components](/develop/api-reference/custom-components)[*arrow\_forward*Next: ComponentRenderer](/develop/api-reference/custom-components/st.components.v2.types.componentrenderer)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI