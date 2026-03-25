<!-- Source: https://docs.streamlit.io/develop/concepts/architecture/run-your-app -->

Working with Streamlit is simple. First you sprinkle a few Streamlit commands into a normal Python script, and then you run it. We list few ways to run your script, depending on your use case.

Once you've created your script, say `your_script.py`, the easiest way to run it is with `streamlit run`:

```
streamlit run your_script.py
```

As soon as you run the script as shown above, a local Streamlit server will spin up and your app will open in a new tab in your default web browser.

When passing your script some custom arguments, they must be passed after two dashes. Otherwise the arguments get interpreted as arguments to Streamlit itself:

```
streamlit run your_script.py [-- script args]
```

You can also pass a URL to `streamlit run`! This is great when your script is hosted remotely, such as a GitHub Gist. For example:

```
streamlit run https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/streamlit_app.py
```

Another way of running Streamlit is to run it as a Python module. This is useful when configuring an IDE like PyCharm to work with Streamlit:

```
# Running
python -m streamlit run your_script.py
```

```
# is equivalent to:
streamlit run your_script.py
```

[*arrow\_back*Previous: Architecture and execution](/develop/concepts/architecture)[*arrow\_forward*Next: Streamlit's architecture](/develop/concepts/architecture/architecture)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI