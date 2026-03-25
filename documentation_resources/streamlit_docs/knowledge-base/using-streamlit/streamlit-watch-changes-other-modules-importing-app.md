<!-- Source: https://docs.streamlit.io/knowledge-base/using-streamlit/streamlit-watch-changes-other-modules-importing-app -->

By default, Streamlit only watches modules contained in the current directory of the main app module. You can track other modules by adding the parent directory of each module to the `PYTHONPATH`.

```
export PYTHONPATH=$PYTHONPATH:/path/to/module
streamlit run your_script.py
```

[*arrow\_back*Previous: Sanity checks](/knowledge-base/using-streamlit/sanity-checks)[*arrow\_forward*Next: What browsers does Streamlit support?](/knowledge-base/using-streamlit/supported-browsers)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI