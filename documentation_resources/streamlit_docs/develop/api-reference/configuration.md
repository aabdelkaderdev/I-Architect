<!-- Source: https://docs.streamlit.io/develop/api-reference/configuration -->

[#### Configuration file

Configures the default settings for your app.

```
your-project/
├── .streamlit/
│   └── config.toml
└── your_app.py
```](/develop/api-reference/configuration/config.toml)[#### Get config option

Retrieve a single configuration option.

```
st.get_option("theme.primaryColor")
```](/develop/api-reference/configuration/st.get_option)[#### Set config option

Set a single configuration option. (This is very limited.)

```
st.set_option("deprecation.showPyplotGlobalUse", False)
```](/develop/api-reference/configuration/st.set_option)[#### Set page title, favicon, and more

Configures the default settings of the page.

```
st.set_page_config(
  page_title="My app",
  page_icon=":shark:",
)
```](/develop/api-reference/configuration/st.set_page_config)

[*arrow\_back*Previous: Custom components](/develop/api-reference/custom-components)[*arrow\_forward*Next: config.toml](/develop/api-reference/configuration/config.toml)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI