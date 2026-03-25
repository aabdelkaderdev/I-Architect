<!-- Source: https://docs.streamlit.io/develop/api-reference/text/st.echo -->

Show API reference for

Version v1.55.0*expand\_more*

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/commands/echo.py#L33 "View st.echo source code on GitHub") | |
| --- | --- |
| st.echo(code\_location="above") | |
| Parameters | |
| code\_location ("above" or "below") | Whether to show the echoed code before or after the results of the executed code block. |

#### Example

```
import streamlit as st

with st.echo():
    st.write('This code will be printed')
```

Sometimes you want your Streamlit app to contain *both* your usual
Streamlit graphic elements *and* the code that generated those elements.
That's where `st.echo()` comes in.

Ok so let's say you have the following file, and you want to make its
app a little bit more self-explanatory by making that middle section
visible in the Streamlit app:

```
import streamlit as st

def get_user_name():
    return 'John'

# ------------------------------------------------
# Want people to see this part of the code...

def get_punctuation():
    return '!!!'

greeting = "Hi there, "
user_name = get_user_name()
punctuation = get_punctuation()

st.write(greeting, user_name, punctuation)

# ...up to here
# ------------------------------------------------

foo = 'bar'
st.write('Done!')
```

The file above creates a Streamlit app containing the words "Hi there,
`John`", and then "Done!".

Now let's use `st.echo()` to make that middle section of the code visible
in the app:

```
import streamlit as st

def get_user_name():
    return 'John'

with st.echo():
    # Everything inside this block will be both printed to the screen
    # and executed.

    def get_punctuation():
        return '!!!'

    greeting = "Hi there, "
    value = get_user_name()
    punctuation = get_punctuation()

    st.write(greeting, value, punctuation)

# And now we're back to _not_ printing to the screen
foo = 'bar'
st.write('Done!')
```

It's *that* simple!

You can have multiple `st.echo()` blocks in the same file.
Use it as often as you wish!

[*arrow\_back*Previous: st.divider](/develop/api-reference/text/st.divider)[*arrow\_forward*Next: st.latex](/develop/api-reference/text/st.latex)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI