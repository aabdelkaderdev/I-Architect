<!-- Source: https://docs.streamlit.io/develop/tutorials/multipage/dynamic-navigation -->

`st.navigation` makes it easy to build dynamic navigation menus. You can change the set of pages passed to `st.navigation` with each rerun, which changes the navigation menu to match. This is a convenient feature for creating custom, role-based navigation menus.

This tutorial uses `st.navigation` and `st.Page`, which were introduced in Streamlit version 1.36.0. For an older workaround using the `pages/` directory and `st.page_link`, see [Build a custom navigation menu with `st.page_link`](/develop/tutorials/multipage/st.page_link-nav).

- Use `st.navigation` and `st.Page` to define a multipage app.
- Create a dynamic, role-based navigation menu.

- This tutorial requires the following version of Streamlit:

  ```
  streamlit>=1.36.0
  ```
- You should have a clean working directory called `your-repository`.
- You should have a basic understanding of `st.navigation` and `st.Page`.

In this example, we'll build a dynamic navigation menu for a multipage app that depends on the current user's role. You'll abstract away the use of username and credentials to simplify the example. Instead, you'll use a selectbox to let users choose a role and log in.

The entrypoint file, `streamlit_app.py` will handle user authentication. The other pages will be stubs representing account management (`settings.py`) and specific pages associated to three roles: Requester, Responder, and Admin. Requesters can access the account and request pages. Responders can access the account and respond pages. Admins can access all pages.

Here's a look at what we'll build:

Complete code*expand\_more*

**Directory structure:**

```
your-repository/
├── admin
│   ├── admin_1.py
│   └── admin_2.py
├── images
│   ├── horizontal_blue.png
│   └── icon_blue.png
├── request
│   ├── request_1.py
│   └── request_2.py
├── respond
│   ├── respond_1.py
│   └── respond_2.py
├── settings.py
└── streamlit_app.py
```

**`streamlit_app.py`:**

```
import streamlit as st

if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None, "Requester", "Responder", "Admin"]

def login():

    st.header("Log in")
    role = st.selectbox("Choose your role", ROLES)

    if st.button("Log in"):
        st.session_state.role = role
        st.rerun()

def logout():
    st.session_state.role = None
    st.rerun()

role = st.session_state.role

logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
settings = st.Page("settings.py", title="Settings", icon=":material/settings:")
request_1 = st.Page(
    "request/request_1.py",
    title="Request 1",
    icon=":material/help:",
    default=(role == "Requester"),
)
request_2 = st.Page(
    "request/request_2.py", title="Request 2", icon=":material/bug_report:"
)
respond_1 = st.Page(
    "respond/respond_1.py",
    title="Respond 1",
    icon=":material/healing:",
    default=(role == "Responder"),
)
respond_2 = st.Page(
    "respond/respond_2.py", title="Respond 2", icon=":material/handyman:"
)
admin_1 = st.Page(
    "admin/admin_1.py",
    title="Admin 1",
    icon=":material/person_add:",
    default=(role == "Admin"),
)
admin_2 = st.Page("admin/admin_2.py", title="Admin 2", icon=":material/security:")

account_pages = [logout_page, settings]
request_pages = [request_1, request_2]
respond_pages = [respond_1, respond_2]
admin_pages = [admin_1, admin_2]

st.title("Request manager")
st.logo("images/horizontal_blue.png", icon_image="images/icon_blue.png")

page_dict = {}
if st.session_state.role in ["Requester", "Admin"]:
    page_dict["Request"] = request_pages
if st.session_state.role in ["Responder", "Admin"]:
    page_dict["Respond"] = respond_pages
if st.session_state.role == "Admin":
    page_dict["Admin"] = admin_pages

if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login)])

pg.run()
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-dynamic-navigation.streamlit.app/?utm_medium=oembed)

1. In `your_repository`, create a file named `streamlit_app.py`.
2. In a terminal, change directories to `your_repository`, and start your app:

   ```
   streamlit run streamlit_app.py
   ```

   Your app will be blank because you still need to add code.
3. In `streamlit_app.py`, write the following:

   ```
   import streamlit as st
   ```
4. Save your `streamlit_app.py` file, and view your running app.
5. In your app, select "**Always rerun**", or press the "**A**" key.

   Your preview will be blank but will automatically update as you save changes to `streamlit_app.py`.
6. Return to your code.

1. In `your_repositoy`, create a file named `settings.py`.
2. In `settings.py` add the following stub.

   ```
   import streamlit as st

   st.header("Settings")
   st.write(f"You are logged in as {st.session_state.role}.")
   ```

   In later steps, you'll create an authentication method that saves the current user's role to `st.session_state.role`. Since you'll be blocking access to this page until a user is logged in, you don't need to initialize the `"role"` key in Session State for this page.
3. Create similar stubs by changing the value of `st.header` for the following six pages:

   ```
   your-repository/
   ├── admin
   │   ├── admin_1.py
   │   └── admin_2.py
   ├── request
   │   ├── request_1.py
   │   └── request_2.py
   └── respond
       ├── respond_1.py
       └── respond_2.py
   ```

   For example, `admin/admin_1.py` should be the following:

   ```
   import streamlit as st

   st.header("Admin 1")
   st.write(f"You are logged in as {st.session_state.role}.")
   ```
4. Create an `images` subdirectory in `your-repository` and add the following two files:

   - [horizontal\_blue.png](/images/horizontal_blue.png)
   - [icon\_blue.png](/images/icon_blue.png)

   You now have all the files needed to build your app.

1. Return to `streamlit_app.py` and initialize `"role"` in Session State.

   ```
   if "role" not in st.session_state:
       st.session_state.role = None
   ```

   You will use this value to gatekeep access to your app. This represents the role of the current, authenticated user.
2. Define the available roles.

   ```
   ROLES = [None, "Requester", "Responder", "Admin"]
   ```

   `None` is included as a role since that is the value corresponding to an unauthenticated user.

`st.navigation` lets you define pages from Python functions. Here, you'll define the login and logout pages from Python functions.

1. Begin your login page (function definition).

   ```
   def login():
   ```
2. Add a header for the page.

   ```
       st.header("Log in")
   ```
3. Create a selectbox for the user to choose a role.

   ```
       role = st.selectbox("Choose your role", ROLES)
   ```
4. Add a button to commit the user role to Session State.

   ```
       if st.button("Log in"):
           st.session_state.role = role
           st.rerun()
   ```

   This is an abstraction of an authentication workflow. When a user clicks the button, Streamlit saves the role to Session State and reruns the app. In later steps, you'll add logic to direct users to a role's default page when the value changes in `st.session_state.role`. This completes your login page function.
5. Begin your logout page (function definition).

   ```
   def logout():
   ```
6. Immediately set the role to `None` and rerun the app.

   ```
       st.session_state.role = None
       st.rerun()
   ```

   Since the lougout page function immediately updates Session State and reruns, a user will never view this page. The page will execute in a fraction of a second and, upon rerunning, the app will send the user to the login page. Therefore, no additional elements are rendered on the page. If desired, you can change this page to also include a button, similar to the login page. A button would allow users to confirm they really intend to log out.

1. As a convenience, save `st.session_state.role` to a variable.

   ```
   role = st.session_state.role
   ```
2. Define your account pages.

   ```
   logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
   settings = st.Page("settings.py", title="Settings", icon=":material/settings:")
   ```

   This gives each page a nice title and icon to make your navigation menu look neat and clean.
3. Define your request pages.

   ```
   request_1 = st.Page(
       "request/request_1.py",
       title="Request 1",
       icon=":material/help:",
       default=(role == "Requester"),
   )
   request_2 = st.Page(
       "request/request_2.py", title="Request 2", icon=":material/bug_report:"
   )
   ```

   If you don't manually declare a default page in `st.navigation`, then the first page will automatically be the default. The first page in the menu will be "Log out" within an "Account" section of the menu. Therefore, you'll need to tell Streamlit what page each user should be directed to by default.

   This code dynamically sets `default=True` when the role is "Requester" and sets it to `False`, otherwise.
4. Define your remaining pages.

   ```
   respond_1 = st.Page(
       "respond/respond_1.py",
       title="Respond 1",
       icon=":material/healing:",
       default=(role == "Responder"),
   )
   respond_2 = st.Page(
       "respond/respond_2.py", title="Respond 2", icon=":material/handyman:"
   )
   admin_1 = st.Page(
       "admin/admin_1.py",
       title="Admin 1",
       icon=":material/person_add:",
       default=(role == "Admin"),
   )
   admin_2 = st.Page("admin/admin_2.py", title="Admin 2", icon=":material/security:")
   ```

   Similar to the request pages, the `default` parameter is set for the other roles' default pages.
5. Group your pages into convenient lists.

   ```
   account_pages = [logout_page, settings]
   request_pages = [request_1, request_2]
   respond_pages = [respond_1, respond_2]
   admin_pages = [admin_1, admin_2]
   ```

   These are all the pages available to logged-in users.

1. Add a title to show on all pages.

   ```
   st.title("Request manager")
   ```

   Since you're calling the title command in your entrypoint file, this title will be visible on all pages. Elements created in your entrypoint file create a frame of common elements around all your pages.
2. Add a logo to your app.

   ```
   st.logo("images/horizontal_blue.png", icon_image="images/icon_blue.png")
   ```

   Once again, since you're calling this command in your entrypoint file, you won't need to also call it within each page.
3. Initialize a dictionary of page lists.

   ```
   page_dict = {}
   ```

   In the next step, you'll check the user's role and add pages to the dictionary that the user is allowed to access. When `st.navigation` receives a dictionary of page lists, it creates a navigation menu with groups of pages and section headers.
4. Build the dictionary of allowed pages by checking the user's role.

   ```
   if st.session_state.role in ["Requester", "Admin"]:
       page_dict["Request"] = request_pages
   if st.session_state.role in ["Responder", "Admin"]:
       page_dict["Respond"] = respond_pages
   if st.session_state.role == "Admin":
       page_dict["Admin"] = admin_pages
   ```
5. Check if the user is allowed to access any pages and add the account pages if they are.

   ```
   if len(page_dict) > 0:
       pg = st.navigation({"Account": account_pages} | page_dict)
   ```

   If `page_dict` is not empty, then the user is logged in. The `|` operator merges the two dictionaries, adding the account pages to the beginning.
6. Fallback to the login page if the user isn't logged in.

   ```
   else:
       pg = st.navigation([st.Page(login)])
   ```
7. Execute the page returned by `st.navigation`.

   ```
   pg.run()
   ```
8. Save your `streamlit_app.py` file and view your app!

   Try logging in, switching pages, and logging out. Try again with a different role.

[*arrow\_back*Previous: Multipage apps](/develop/tutorials/multipage)[*arrow\_forward*Next: Build navigation with st.page\_link](/develop/tutorials/multipage/st.page_link-nav)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI