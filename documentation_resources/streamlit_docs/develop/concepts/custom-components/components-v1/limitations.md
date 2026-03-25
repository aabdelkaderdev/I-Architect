<!-- Source: https://docs.streamlit.io/develop/concepts/custom-components/components-v1/limitations -->

- Streamlit Components are wrapped up in an iframe, which gives you the ability to do whatever you want (within the iframe) using any web technology you like.

Because each Streamlit Component gets mounted into its own sandboxed iframe, this implies a few limitations on what is possible with Components:

- **Can't communicate with other Components**: Components can’t contain (or otherwise communicate with) other components, so Components cannot be used to build something like a grid layout.
- **Can't modify CSS**: A Component can’t modify the CSS that the rest of the Streamlit app uses, so you can't create something to put the app in dark mode, for example.
- **Can't add/remove elements**: A Component can’t add or remove other elements of a Streamlit app, so you couldn't make something to remove the app menu, for example.

Currently, no automatic debouncing of Component updates is performed within Streamlit. The Component creator themselves can decide to rate-limit the updates they send back to Streamlit.

[*arrow\_back*Previous: Create a component](/develop/concepts/custom-components/components-v1/create)[*arrow\_forward*Next: Publish a component](/develop/concepts/custom-components/publish)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI