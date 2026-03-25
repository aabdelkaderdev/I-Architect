<!-- Source: https://docs.streamlit.io/develop/api-reference/custom-components/component-v2-lib-frontendrenderer -->

Show API reference for

Version v1.55.0*expand\_more*

| (TypeScript) Type alias description[[source]](https://github.com/streamlit/streamlit/blob/1.53.0/frontend/component-v2-lib/src/types.ts#L227 "View st.FrontendRenderer source code on GitHub") | |
| --- | --- |
| FrontendRenderer<TState extends FrontendState = FrontendState, TData = unknown> = (componentArgs: FrontendRendererArgs<TState, TData>) => CleanupFunction | void | |
| Arguments | |
| FrontendRendererArgs (FrontendRendererArgs<TState, TData>) | The inputs and utilities provided by Streamlit to your component. |
|  |  |
| --- | --- |
| Returns | |
| (CleanupFunction | void) | An optional cleanup function that Streamlit will call when the component is unmounted. |

[*arrow\_back*Previous: component-v2-lib](/develop/api-reference/custom-components/component-v2-lib)[*arrow\_forward*Next: FrontendRendererArgs](/develop/api-reference/custom-components/component-v2-lib-frontendrendererargs)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI