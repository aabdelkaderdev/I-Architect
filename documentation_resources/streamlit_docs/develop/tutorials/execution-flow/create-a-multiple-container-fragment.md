<!-- Source: https://docs.streamlit.io/develop/tutorials/execution-flow/create-a-multiple-container-fragment -->

Streamlit lets you turn functions into [fragments](/develop/concepts/architecture/fragments), which can rerun independently from the full script. If your fragment doesn't write to outside containers, Streamlit will clear and redraw all the fragment elements with each fragment rerun. However, if your fragment *does* write elements to outside containers, Streamlit will not clear those elements during a fragment rerun. Instead, those elements accumulate with each fragment rerun until the next full-script rerun. If you want a fragment to update multiple containers in your app, use [`st.empty()`](/develop/api-reference/layout/st.empty) containers to prevent accumulating elements.

- Use fragments to run two independent processes separately.
- Distribute a fragment across multiple containers.

- This tutorial requires the following version of Streamlit:

  ```
  streamlit>=1.37.0
  ```
- You should have a clean working directory called `your-repository`.
- You should have a basic understanding of fragments and `st.empty()`.

In this toy example, you'll build an app with six containers. Three containers will have orange cats. The other three containers will have black cats. You'll have three buttons in the sidebar: "**Herd the black cats**," "**Herd the orange cats**," and "**Herd all the cats**." Since herding cats is slow, you'll use fragments to help Streamlit run the associated processes efficiently. You'll create two fragments, one for the black cats and one for the orange cats. Since the buttons will be in the sidebar and the fragments will update containers in the main body, you'll use a trick with `st.empty()` to ensure you don't end up with too many cats in your app (if it's even possible to have too many cats). 😻

Here's a look at what you'll build:

Complete code*expand\_more*

```
import streamlit as st
import time

st.title("Cats!")

row1 = st.columns(3)
row2 = st.columns(3)

grid = [col.container(height=200) for col in row1 + row2]
safe_grid = [card.empty() for card in grid]

def black_cats():
    time.sleep(1)
    st.title("🐈‍⬛ 🐈‍⬛")
    st.markdown("🐾 🐾 🐾 🐾")

def orange_cats():
    time.sleep(1)
    st.title("🐈 🐈")
    st.markdown("🐾 🐾 🐾 🐾")

@st.fragment
def herd_black_cats(card_a, card_b, card_c):
    st.button("Herd the black cats")
    container_a = card_a.container()
    container_b = card_b.container()
    container_c = card_c.container()
    with container_a:
        black_cats()
    with container_b:
        black_cats()
    with container_c:
        black_cats()

@st.fragment
def herd_orange_cats(card_a, card_b, card_c):
    st.button("Herd the orange cats")
    container_a = card_a.container()
    container_b = card_b.container()
    container_c = card_c.container()
    with container_a:
        orange_cats()
    with container_b:
        orange_cats()
    with container_c:
        orange_cats()

with st.sidebar:
    herd_black_cats(grid[0].empty(), grid[2].empty(), grid[4].empty())
    herd_orange_cats(grid[1].empty(), grid[3].empty(), grid[5].empty())
    st.button("Herd all the cats")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-tutorial-fragment-multiple-container.streamlit.app/?utm_medium=oembed)

1. In `your_repository`, create a file named `app.py`.
2. In a terminal, change directories to `your_repository`, and start your app:

   ```
   streamlit run app.py
   ```

   Your app will be blank because you still need to add code.
3. In `app.py`, write the following:

   ```
   import streamlit as st
   import time
   ```

   You'll use `time.sleep()` to slow things down and see the fragments working.
4. Save your `app.py` file, and view your running app.
5. In your app, select "**Always rerun**", or press the "**A**" key.

   Your preview will be blank but will automatically update as you save changes to `app.py`.
6. Return to your code.

1. Add a title to your app and two rows of three containers.

   ```
   st.title("Cats!")

   row1 = st.columns(3)
   row2 = st.columns(3)

   grid = [col.container(height=200) for col in row1 + row2]
   ```

   Save your file to see your updated preview.
2. Define a helper function to draw two black cats.

   ```
   def black_cats():
       time.sleep(1)
       st.title("🐈‍⬛ 🐈‍⬛")
       st.markdown("🐾 🐾 🐾 🐾")
   ```

   This function represents "herding two cats" and uses `time.sleep()` to simulate a slower process. You will use this to draw two cats in one of your grid cards later on.
3. Define another helper function to draw two orange cats.

   ```
   def orange_cats():
       time.sleep(1)
       st.title("🐈 🐈")
       st.markdown("🐾 🐾 🐾 🐾")
   ```
4. Optional: Test out your functions by calling each one within a grid card.

   ```
   with grid[0]:
       black_cats()
   with grid[1]:
       orange_cats()
   ```

   Save your `app.py` file to see the preview. Delete these four lines when finished.

Since each fragment will span across the sidebar and three additional containers, you'll use the sidebar to hold the main body of the fragment and pass the three containers as function arguments.

1. Use an [`@st.fragment`](/develop/api-reference/execution-flow/st.fragment) decorator and start your black-cat fragment definition.

   ```
   @st.fragment
   def herd_black_cats(card_a, card_b, card_c):
   ```
2. Add a button for rerunning this fragment.

   ```
       st.button("Herd the black cats")
   ```
3. Write to each container using your helper function.

   ```
       with card_a:
           black_cats()
       with card_b:
           black_cats()
       with card_c:
           black_cats()
   ```

   **This code above will not behave as desired, but you'll explore and correct this in the following steps.**
4. Test out your code. Call your fragment function in the sidebar.

   ```
   with st.sidebar:
       herd_black_cats(grid[0], grid[2], grid[4])
   ```

   Save your file and try using the button in the sidebar. More and more cats are appear in the cards with each fragment rerun! This is the expected behavior when fragments write to outside containers. To fix this, you will pass `st.empty()` containers to your fragment function.
5. Delete the lines of code from the previous two steps.
6. To prepare for using `st.empty()` containers, correct your cat-herding function as follows. After the button, define containers to place in the `st.empty()` cards you'll pass to your fragment.

   ```
       container_a = card_a.container()
       container_b = card_b.container()
       container_c = card_c.container()
       with container_a:
           black_cats()
       with container_b:
           black_cats()
       with container_c:
           black_cats()
   ```

   In this new version, `card_a`, `card_b`, and `card_c` will be `st.empty()` containers. You create `container_a`, `container_b`, and `container_c` to allow Streamlit to draw multiple elements on each grid card.
7. Similarly define your orange-cat fragment function.

   ```
   @st.fragment
   def herd_orange_cats(card_a, card_b, card_c):
       st.button("Herd the orange cats")
       container_a = card_a.container()
       container_b = card_b.container()
       container_c = card_c.container()
       with container_a:
           orange_cats()
       with container_b:
           orange_cats()
       with container_c:
           orange_cats()
   ```

1. Call both of your fragments in the sidebar.

   ```
   with st.sidebar:
       herd_black_cats(grid[0].empty(), grid[2].empty(), grid[4].empty())
       herd_orange_cats(grid[1].empty(), grid[3].empty(), grid[5].empty())
   ```

   By creating `st.empty()` containers in each card and passing them to your fragments, you prevent elements from accumulating in the cards with each fragment rerun. If you create the `st.empty()` containers earlier in your app, full-script reruns will clear the orange-cat cards while (first) rendering the black-cat cards.
2. Include a button outside of your fragments. When clicked, the button will trigger a full-script rerun since you're calling its widget function outside of any fragment.

   ```
       st.button("Herd all the cats")
   ```
3. Save your file and try out the app! When you click "**Herd the black cats**" or "**Herd the orange cats**," Streamlit will only redraw the three related cards. When you click "**Herd all the cats**," Streamlit redraws all six cards.

[*arrow\_back*Previous: Rerun your app from a fragment](/develop/tutorials/execution-flow/trigger-a-full-script-rerun-from-a-fragment)[*arrow\_forward*Next: Start and stop a streaming fragment](/develop/tutorials/execution-flow/start-and-stop-fragment-auto-reruns)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI