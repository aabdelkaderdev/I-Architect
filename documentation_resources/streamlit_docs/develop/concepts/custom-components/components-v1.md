<!-- Source: https://docs.streamlit.io/develop/concepts/custom-components/components-v1 -->

Components are third-party Python modules that extend what's possible with Streamlit.

Components are super easy to use:

1. Start by finding the Component you'd like to use. Two great resources for this are:

   - The [Component gallery](https://streamlit.io/components)
   - [This thread](https://discuss.streamlit.io/t/streamlit-components-community-tracker/4634),
     by Fanilo A. from our forums.
2. Install the Component using your favorite Python package manager. This step and all following
   steps are described in your component's instructions.

   For example, to use the fantastic [AgGrid
   Component](https://github.com/PablocFonseca/streamlit-aggrid), you first install it with:

   ```
   pip install streamlit-aggrid
   ```
3. In your Python code, import the Component as described in its instructions. For AgGrid, this step
   is:

   ```
   from st_aggrid import AgGrid
   ```
4. ...now you're ready to use it! For AgGrid, that's:

   ```
   AgGrid(my_dataframe)
   ```

If you're interested in making your own component, check out the following resources:

- [Create a Component](/develop/concepts/custom-components/components-v1/create)
- [Publish a Component](/develop/concepts/custom-components/publish)
- [Components API](/develop/concepts/custom-components/components-v1/intro)
- [Blog post for when we launched Components!](https://blog.streamlit.io/introducing-streamlit-components/)

Alternatively, if you prefer to learn using videos, our engineer Tim Conkling has put together some
amazing tutorials:

##### Video tutorial, part 1

##### Video tutorial, part 2

[*arrow\_back*Previous: Components v2](/develop/concepts/custom-components/components-v2)[*arrow\_forward*Next: Intro to v1 components](/develop/concepts/custom-components/components-v1/intro)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI