<!-- Source: https://docs.streamlit.io/develop/api-reference/custom-components -->

Streamlit custom components extend your app beyond built-in widgets with custom UI elements. V2 components offer better performance and multiple callbacks without iframes, while V1 components run in iframes with single callbacks.

[#### Register

Register a custom component.

```
my_component = st.components.v2.component(
    html=HTML,
    js=JS
)
my_component()
```](/develop/api-reference/custom-components/st.components.v2.component)[#### Mount

Mount a custom component.

```
my_component = st.components.v2.component(
    html=HTML,
    js=JS
)
my_component()
```](/develop/api-reference/custom-components/st.components.v2.types.componentrenderer)

[#### npm support code

Support code published through npm.

```
npm i @streamlit/component-v2-lib
```](/develop/api-reference/custom-components/component-v2-lib)[#### FrontendRenderer

Type alias for the component function.

```
import { FrontendRenderer } from "@streamlit/component-v2-lib";
```](/develop/api-reference/custom-components/component-v2-lib-frontendrenderer)[#### FrontendRendererArgs

Type alias for the component arguments.

```
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
```](/develop/api-reference/custom-components/component-v2-lib-frontendrendererargs)[#### FrontendState

Type alias for the component state.

```
import { FrontendState } from "@streamlit/component-v2-lib";
```](/develop/api-reference/custom-components/component-v2-lib-frontendstate)[#### CleanupFunction

Type alias for the component cleanup function.

```
import { CleanupFunction } from "@streamlit/component-v2-lib";
```](/develop/api-reference/custom-components/component-v2-lib-cleanupfunction)

[#### Declare a component

Create and register a custom component.

```
from st.components.v1 import declare_component
declare_component(
    "custom_slider",
    "/frontend",
)
```](/develop/api-reference/custom-components/st.components.v1.declare_component)[#### HTML

Display an HTML string in an iframe.

```
from st.components.v1 import html
html(
    "<p>Foo bar.</p>"
)
```](/develop/api-reference/custom-components/st.components.v1.html)[#### iframe

Load a remote URL in an iframe.

```
from st.components.v1 import iframe
iframe(
    "docs.streamlit.io"
)
```](/develop/api-reference/custom-components/st.components.v1.iframe)

[*arrow\_back*Previous: Connections and secrets](/develop/api-reference/connections)[*arrow\_forward*Next: component](/develop/api-reference/custom-components/st.components.v2.component)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI