<!-- Source: https://docs.streamlit.io/develop/api-reference/cli/init -->

This command creates the files for a new Streamlit app.

```
streamlit init <directory>
```

`<directory>` (Optional): The directory location of the new project. If no directory is provided, the current working directory will be used.

#### Example 1: Create project files the current working directory

1. In your current working directory (CWD), execute the following:

   ```
   streamlit init
   ```

   Streamlit creates the following files:

   ```
   CWD/
   ├── requirements.txt
   └── streamlit_app.py
   ```
2. In your terminal, Streamlit prompts, `❓ Run the app now? [Y/n]`. Enter `Y` for yes.

   This is equivalent to executing `streamlit run streamlit_app.py` from your current working directory.
3. Begin editing your `streamlit_app.py` file and save your changes.

#### Example 2: Create project files in another directory

1. In your current working directory (CWD), execute the following:

   ```
   streamlit init project
   ```

   Streamlit creates the following files:

   ```
   CWD/
   └── project/
       ├── requirements.txt
       └── streamlit_app.py
   ```
2. In your terminal, Streamlit prompts, `❓ Run the app now? [Y/n]`. Enter `Y` for yes.

   This is equivalent to executing `streamlit run project/streamlit_app.py` from your current working directory.
3. Begin editing your `streamlit_app.py` file and save your changes.

[*arrow\_back*Previous: streamlit help](/develop/api-reference/cli/help)[*arrow\_forward*Next: streamlit run](/develop/api-reference/cli/run)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI