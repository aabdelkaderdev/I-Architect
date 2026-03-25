<!-- Source: https://docs.streamlit.io/develop/concepts/configuration/serving-static-files -->

Streamlit apps can host and serve small, static media files to support media embedding use cases that
won't work with the normal [media elements](/develop/api-reference/media).

To enable this feature, set `enableStaticServing = true` under `[server]` in your config file,
or environment variable `STREAMLIT_SERVER_ENABLE_STATIC_SERVING=true`.

Media stored in the folder `./static/` relative to the running app file is served at path
`app/static/[filename]`, such as `http://localhost:8501/app/static/cat.png`.

- Files with the following extensions will be served normally:
  - Common image types: `.jpg`, `.jpeg`, `.png`, `.gif`
  - Common font types: `.otf`, `.ttf`, `.woff`, `.woff2`
  - Other types: `.pdf`, `.xml`, `.json`
    Any other file will be sent with header `Content-Type:text/plain` which will cause browsers to render in plain text.
    This is included for security - other file types that need to render should be hosted outside the app.
- Streamlit also sets `X-Content-Type-Options:nosniff` for all files rendered from the static directory.
- For apps running on Streamlit Community Cloud:
  - Files available in the Github repo will always be served. Any files generated while the app is running,
    such as based on user interaction (file upload, etc), are not guaranteed to persist across user sessions.
  - Apps which store and serve many files, or large files, may run into resource limits and be shut down.

- Put an image `cat.png` in the folder `./static/`
- Add `enableStaticServing = true` under `[server]` in your `.streamlit/config.toml`
- Any media in the `./static/` folder is served at the relative URL like `app/static/cat.png`

```
# .streamlit/config.toml

[server]
enableStaticServing = true
```

```
# app.py
import streamlit as st

with st.echo():
    st.title("CAT")

    st.markdown("[![Click me](app/static/cat.png)](https://streamlit.io)")
```

Additional resources:

- <https://docs.streamlit.io/develop/concepts/configuration>
- <https://static-file-serving.streamlit.app/>

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://static-file-serving.streamlit.app/?utm_medium=oembed)

[*arrow\_back*Previous: HTTPS support](/develop/concepts/configuration/https-support)[*arrow\_forward*Next: Customize your theme](/develop/concepts/configuration/theming)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI