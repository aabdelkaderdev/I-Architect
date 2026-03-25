<!-- Source: https://docs.streamlit.io/knowledge-base/deploy/increase-file-uploader-limit-streamlit-cloud -->

By default, files uploaded using [`st.file_uploader()`](/develop/api-reference/widgets/st.file_uploader) are limited to 200MB. You can configure this using the `server.maxUploadSize` config option.

Streamlit provides [four different ways to set configuration options](/develop/concepts/configuration):

1. In a **global config file** at `~/.streamlit/config.toml` for macOS/Linux or `%userprofile%/.streamlit/config.toml` for Windows:

   ```
   [server]
   maxUploadSize = 200
   ```
2. In a **per-project config file** at `$CWD/.streamlit/config.toml`, where `$CWD` is the folder you're running Streamlit from.
3. Through `STREAMLIT_*` **environment variables**, such as:

   ```
   export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200
   ```
4. As **flags on the command line** when running `streamlit run`:

   ```
   streamlit run your_script.py --server.maxUploadSize 200
   ```

Which of the four options should you choose for an app deployed to [Streamlit Community Cloud](/deploy/streamlit-community-cloud)? 🤔

When deploying your app to Streamlit Community Cloud, you should **use option 1**. Namely, set the `maxUploadSize` config option in a global config file (`.streamlit/config.toml`) uploaded to your app's GitHub repo. 🎈

For example, to increase the upload limit to 400MB, upload a `.streamlit/config.toml` file containing the following lines to your app's GitHub repo:

```
[server]
maxUploadSize = 400
```

- [Streamlit drag and drop capping at 200MB, need workaround](https://discuss.streamlit.io/t/streamlit-drag-and-drop-capping-at-200mb-need-workaround/19803/2)
- [File uploader widget API](/develop/api-reference/widgets/st.file_uploader)
- [How to set Streamlit configuration options](/develop/concepts/configuration)

[*arrow\_back*Previous: Does Streamlit support the WSGI Protocol? (aka Can I deploy Streamlit with gunicorn?)](/knowledge-base/deploy/does-streamlit-support-wsgi-protocol)[*arrow\_forward*Next: Invoking a Python subprocess in a deployed Streamlit app](/knowledge-base/deploy/invoking-python-subprocess-deployed-streamlit-app)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI