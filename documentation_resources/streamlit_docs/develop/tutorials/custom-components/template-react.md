<!-- Source: https://docs.streamlit.io/develop/tutorials/custom-components/template-react -->

In this tutorial, you'll use the official [component template](https://github.com/streamlit/component-template) to generate a React-based custom component. You'll learn how React integrates with Streamlit's component lifecycle, how to manage the React root, and how to extend the template with React hooks and JSX.

- The following packages must be installed in your Python environment:

  ```
  streamlit>=1.51.0
  uv
  ```
- Node.js 24 or later must be installed. This includes npm, the package manager for JavaScript.
- Familiarity with [React](https://react.dev/) basics (components, hooks, JSX) is recommended.
- Familiarity with [inline custom components](/develop/concepts/custom-components/components-v2/examples) is recommended.

The template generates a working "Hello, World!" component with a click counter built using React. You'll walk through the generated code, then extend it to render a dynamic list of items from Python data.

Here's a look at what you'll build:

Complete modified files*expand\_more*

```
my-react-counter/
├── pyproject.toml
├── example.py
└── my_react_counter/
    ├── __init__.py
    ├── pyproject.toml
    └── frontend/
        ├── package.json
        ├── tsconfig.json
        ├── vite.config.ts
        └── src/
            ├── index.tsx
            └── MyComponent.tsx
```

```
import streamlit as st

out = st.components.v2.component(
    "my-react-counter.my_react_counter",
    js="index-*.js",
    html='<div class="react-root"></div>',
)

def my_react_counter(name, items=None, key=None, on_item_clicked=lambda: None):
    component_value = out(
        key=key,
        default={"num_clicks": 0, "selected_item": None},
        data={"name": name, "items": items or []},
        on_num_clicks_change=lambda: None,
        on_selected_item_change=lambda: None,
        on_item_clicked_change=on_item_clicked,
    )
    return component_value
```

```
import {
  FrontendRenderer,
  FrontendRendererArgs,
} from "@streamlit/component-v2-lib";
import { StrictMode } from "react";
import { createRoot, Root } from "react-dom/client";

import MyComponent, {
  MyComponentDataShape,
  MyComponentStateShape,
} from "./MyComponent";

const reactRoots: WeakMap<FrontendRendererArgs["parentElement"], Root> =
  new WeakMap();

const MyComponentRoot: FrontendRenderer<
  MyComponentStateShape,
  MyComponentDataShape
> = (args) => {
  const { data, parentElement, setStateValue, setTriggerValue } = args;

  const rootElement = parentElement.querySelector(".react-root");

  if (!rootElement) {
    throw new Error("Unexpected: React root element not found");
  }

  let reactRoot = reactRoots.get(parentElement);
  if (!reactRoot) {
    reactRoot = createRoot(rootElement);
    reactRoots.set(parentElement, reactRoot);
  }

  const { name, items } = data;

  reactRoot.render(
    <StrictMode>
      <MyComponent
        name={name}
        items={items}
        setStateValue={setStateValue}
        setTriggerValue={setTriggerValue}
      />
    </StrictMode>,
  );

  return () => {
    const reactRoot = reactRoots.get(parentElement);

    if (reactRoot) {
      reactRoot.unmount();
      reactRoots.delete(parentElement);
    }
  };
};

export default MyComponentRoot;
```

```
import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { FC, ReactElement, useCallback, useState } from "react";

export type MyComponentStateShape = {
  num_clicks: number;
  selected_item: string | null;
  item_clicked: string | null;
};

export type MyComponentDataShape = {
  name: string;
  items: string[];
};

export type MyComponentProps = Pick<
  FrontendRendererArgs<MyComponentStateShape, MyComponentDataShape>,
  "setStateValue" | "setTriggerValue"
> &
  MyComponentDataShape;

const MyComponent: FC<MyComponentProps> = ({
  name,
  items,
  setStateValue,
  setTriggerValue,
}): ReactElement => {
  const [numClicks, setNumClicks] = useState(0);
  const [selectedItem, setSelectedItem] = useState<string | null>(null);

  const onClicked = useCallback((): void => {
    const newNumClicks = numClicks + 1;
    setNumClicks(newNumClicks);
    setStateValue("num_clicks", newNumClicks);
  }, [numClicks, setStateValue]);

  const onItemSelected = useCallback(
    (item: string): void => {
      setSelectedItem(item);
      setStateValue("selected_item", item);
      setTriggerValue("item_clicked", item);
    },
    [setStateValue, setTriggerValue],
  );

  return (
    <div>
      <h2>Hello, {name}!</h2>
      <button onClick={onClicked} style={{ cursor: "pointer" }}>
        Clicked {numClicks} times
      </button>
      {items && items.length > 0 && (
        <ul>
          {items.map((item) => (
            <li
              key={item}
              onClick={() => onItemSelected(item)}
              style={{
                cursor: "pointer",
                background:
                  selectedItem === item
                    ? "var(--st-primary-color)"
                    : "var(--st-secondary-background-color)",
              }}
            >
              {item}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default MyComponent;
```

```
import streamlit as st
from my_react_counter import my_component

st.title("My React Counter")

result = my_component(
    "Streamlit",
    items=["Python", "TypeScript", "React", "Vite"],
    key="counter",
)

st.write(f"Click count: {result.num_clicks}")
if result.selected_item:
    st.write(f"Selected: {result.selected_item}")
if result.item_clicked:
    st.write(f"Just clicked: {result.item_clicked}")
```

1. Navigate to the directory where you want to create your project and run the cookiecutter generator. The generator will create a new subdirectory for your project.

   ```
   uvx --from cookiecutter cookiecutter gh:streamlit/component-template --directory cookiecutter/v2
   ```
2. Follow the interactive prompts. When asked for the framework, select **React + Typescript**:

   ```
   [1/8] author_name (John Smith): Your Name
   [2/8] author_email (john@example.com): you@example.com
   [3/8] project_name (Streamlit Component X): My React Counter
   [4/8] package_name (streamlit-component-x): my-react-counter
   [5/8] import_name (streamlit_component_x): my_react_counter
   [6/8] description (Streamlit component that allows you to do X): A React-based counter component
   [7/8] Select open_source_license
     ...
     Choose from [1/2/3/4/5/6](1): 1
   [8/8] Select framework
     1 - React + Typescript
     2 - Pure Typescript
     Choose from [1/2] (1): 1
   ```

   This creates a `my-react-counter/` directory with the following structure:

   ```
   my-react-counter/
   ├── example.py
   ├── LICENSE
   ├── MANIFEST.in
   ├── pyproject.toml
   ├── README.md
   └── my_react_counter/
       ├── __init__.py
       ├── pyproject.toml
       └── frontend/
           ├── package.json
           ├── tsconfig.json
           ├── vite.config.ts
           └── src/
               ├── index.tsx
               ├── MyComponent.tsx
               └── vite-env.d.ts
   ```

   Notice the React template has two frontend source files instead of one: `index.tsx` handles integration with Streamlit's lifecycle, and `MyComponent.tsx` contains the React component. This is a convention but not a requirement. You can have a single source file or arbitrarily many source files.

You need two terminals running in parallel for development. The following steps use `uv run` to run commands inside the project's virtual environment. If a `.venv` doesn't exist yet, `uv run` creates one automatically.

1. In the first terminal, navigate to the frontend directory, install dependencies, and start the dev build watcher:

   ```
   cd my-react-counter/my_react_counter/frontend
   npm install
   npm run dev
   ```
2. In a second terminal, navigate to the project root and run the example app:

   ```
   cd my-react-counter
   uv run streamlit run example.py
   ```
3. View your running app.

   You should see a "Hello, World!" heading with a "Click Me!" button. Clicking the button increments a counter that's sent back to Python. An `st.text_input` lets you specify a name which is passed to a second instance of the component.

Now that the component is running, walk through each file to understand how it works.

1. Open `my_react_counter/__init__.py`:

   ```
   import streamlit as st

   out = st.components.v2.component(
       "my-react-counter.my_react_counter",
       js="index-*.js",
       html='<div class="react-root"></div>',
   )

   def on_num_clicks_change():
       pass

   def my_react_counter(name, key=None):
       component_value = out(
           name=name,
           key=key,
           default={"num_clicks": 0},
           data={"name": name},
           on_num_clicks_change=on_num_clicks_change,
       )

       return component_value
   ```

   This file does two things:

   - **Registers the component** with `st.components.v2.component()`. The first argument is a qualified name (`"<package-name>.<component-name>"`) where `<package-name>` matches the `name` field in the project-level `pyproject.toml` and `<component-name>` matches the `name` field in the component-level `pyproject.toml`. The other two arguments point to the frontend assets: `js` is a glob pattern that matches the JavaScript bundle produced by Vite. `html` provides the root `<div>` that React mounts into.
   - **Defines a wrapper function** (`my_react_counter`) that provides a clean API. The wrapper calls the raw component with `data`, `default`, and callback parameters. This pattern is optional but recommended. For more about these parameters, see [Component mounting](/develop/concepts/custom-components/components-v2/mount).
2. Open `my_react_counter/frontend/src/index.tsx`:

   ```
   import {
     FrontendRenderer,
     FrontendRendererArgs,
   } from "@streamlit/component-v2-lib";
   import { StrictMode } from "react";
   import { createRoot, Root } from "react-dom/client";

   import MyComponent, {
     MyComponentDataShape,
     MyComponentStateShape,
   } from "./MyComponent";

   const reactRoots: WeakMap<FrontendRendererArgs["parentElement"], Root> =
     new WeakMap();

   const MyComponentRoot: FrontendRenderer<
     MyComponentStateShape,
     MyComponentDataShape
   > = (args) => {
     const { data, parentElement, setStateValue } = args;

     const rootElement = parentElement.querySelector(".react-root");

     if (!rootElement) {
       throw new Error("Unexpected: React root element not found");
     }

     let reactRoot = reactRoots.get(parentElement);
     if (!reactRoot) {
       reactRoot = createRoot(rootElement);
       reactRoots.set(parentElement, reactRoot);
     }

     const { name } = data;

     reactRoot.render(
       <StrictMode>
         <MyComponent setStateValue={setStateValue} name={name} />
       </StrictMode>,
     );

     return () => {
       const reactRoot = reactRoots.get(parentElement);

       if (reactRoot) {
         reactRoot.unmount();
         reactRoots.delete(parentElement);
       }
     };
   };

   export default MyComponentRoot;
   ```

   This file bridges Streamlit's component lifecycle and React. Because Streamlit calls your `FrontendRenderer` function on every re-render (whenever `data` changes), the pattern is different from a typical React app:

   - **React root management**: You can't create a new React root each time Streamlit calls your function because that would destroy React state on every update. Instead, the `WeakMap` stores one root per component instance, keyed by `parentElement`. On the first call, it creates the root. On subsequent calls, it re-renders into the existing root. This also means multiple instances of the same component in an app each get their own independent React root with their own state.
   - **Module-level scope**: Code outside `MyComponentRoot`, like the `WeakMap` declaration, runs once when the module loads and is shared across all component instances. If you need one-time global setup. like initializing a third-party library, put it at the module level so it's done once rather than repeated per instance or per re-render.
   - **Passing props**: `MyComponentRoot` extracts `data` and `setStateValue` from Streamlit's args and passes them as React props to `MyComponent`. This is where you decide which Streamlit args your React component needs.
   - **Cleanup**: The returned function unmounts the React root when Streamlit removes the component from the page.
3. Open `my_react_counter/frontend/src/MyComponent.tsx`:

   ```
   import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
   import {
     CSSProperties,
     FC,
     ReactElement,
     useCallback,
     useMemo,
     useState,
   } from "react";

   export type MyComponentStateShape = {
     num_clicks: number;
   };

   export type MyComponentDataShape = {
     name: string;
   };

   export type MyComponentProps = Pick<
     FrontendRendererArgs<MyComponentStateShape, MyComponentDataShape>,
     "setStateValue"
   > &
     MyComponentDataShape;

   const MyComponent: FC<MyComponentProps> = ({
     name,
     setStateValue,
   }): ReactElement => {
     const [isFocused, setIsFocused] = useState(false);
     const [numClicks, setNumClicks] = useState(0);

     const style = useMemo<CSSProperties>(() => {
       const colorToUse = isFocused
         ? "var(--st-primary-color)"
         : "var(--st-gray-color)";

       const borderStyling = `1px solid ${colorToUse}`;

       return {
         border: borderStyling,
         outline: borderStyling,
       };
     }, [isFocused]);

     const onClicked = useCallback((): void => {
       const newNumClicks = numClicks + 1;
       setNumClicks(newNumClicks);

       setStateValue("num_clicks", newNumClicks);
     }, [numClicks, setStateValue]);

     const onFocus = useCallback((): void => {
       setIsFocused(true);
     }, []);

     const onBlur = useCallback((): void => {
       setIsFocused(false);
     }, []);

     return (
       <span>
         <h1>Hello, {name}!</h1>
         <button
           style={style}
           onClick={onClicked}
           // disabled={disabled}
           onFocus={onFocus}
           onBlur={onBlur}
         >
           Click Me!
         </button>
       </span>
     );
   };

   export default MyComponent;
   ```

   This is a standard React functional component:

   - **Type-safe props**: `MyComponentProps` is constructed from `FrontendRendererArgs` using TypeScript's `Pick` utility type. This ensures the `setStateValue` prop is correctly typed for the component's state shape.
   - **React state management**: Local UI state (like `isFocused`) is managed with React's `useState` hook. This state is purely for the frontend and doesn't need to go back to Python.
   - **Communicating with Python**: When the button is clicked, `setStateValue("num_clicks", newNumClicks)` sends the count back to Streamlit. This triggers a Python rerun, just like in non-React components.
   - **Streamlit theming**: The component uses CSS custom properties like `var(--st-primary-color)` directly in inline styles. These properties are provided by Streamlit's theme system and work inside the component's shadow DOM.

Now extend the template to render a dynamic list of items from Python data. This showcases something React does well: declaratively rendering lists with state.

1. In `my_react_counter/frontend/src/MyComponent.tsx`, make the following changes to add list rendering and item selection:

   The copy button on the diff code blocks only copy the lines in the final result, not the deleted lines.

   ```
   =import { FrontendRendererArgs } from "@streamlit/component-v2-lib";
   -import {
   -  CSSProperties,
   -  FC,
   -  ReactElement,
   -  useCallback,
   -  useMemo,
   -  useState,
   -} from "react";
   +import { FC, ReactElement, useCallback, useState } from "react";
   =
   =export type MyComponentStateShape = {
   =  num_clicks: number;
   +  selected_item: string | null;
   +  item_clicked: string | null;
   =};
   =
   =export type MyComponentDataShape = {
   =  name: string;
   +  items: string[];
   =};
   =
   =export type MyComponentProps = Pick<
   =  FrontendRendererArgs<MyComponentStateShape, MyComponentDataShape>,
   -  "setStateValue"
   +  "setStateValue" | "setTriggerValue"
   => &
   =  MyComponentDataShape;
   =
   =const MyComponent: FC<MyComponentProps> = ({
   =  name,
   +  items,
   =  setStateValue,
   +  setTriggerValue,
   =}): ReactElement => {
   -  const [isFocused, setIsFocused] = useState(false);
   =  const [numClicks, setNumClicks] = useState(0);
   +  const [selectedItem, setSelectedItem] = useState<string | null>(null);
   -
   -  const style = useMemo<CSSProperties>(() => {
   -    const colorToUse = isFocused
   -      ? "var(--st-primary-color)"
   -      : "var(--st-gray-color)";
   -
   -    const borderStyling = `1px solid ${colorToUse}`;
   -
   -    return {
   -      border: borderStyling,
   -      outline: borderStyling,
   -    };
   -  }, [isFocused]);
   =
   =  const onClicked = useCallback((): void => {
   =    const newNumClicks = numClicks + 1;
   =    setNumClicks(newNumClicks);
   =    setStateValue("num_clicks", newNumClicks);
   =  }, [numClicks, setStateValue]);
   =
   -  const onFocus = useCallback((): void => {
   -    setIsFocused(true);
   -  }, []);
   -
   -  const onBlur = useCallback((): void => {
   -    setIsFocused(false);
   -  }, []);
   -
   -  return (
   -    <span>
   -      <h1>Hello, {name}!</h1>
   -      <button
   -        style={style}
   -        onClick={onClicked}
   -        // disabled={disabled}
   -        onFocus={onFocus}
   -        onBlur={onBlur}
   -      >
   -        Click Me!
   -      </button>
   -    </span>
   -  );
   +  const onItemSelected = useCallback(
   +    (item: string): void => {
   +      setSelectedItem(item);
   +      setStateValue("selected_item", item);
   +      setTriggerValue("item_clicked", item);
   +    },
   +    [setStateValue, setTriggerValue],
   +  );
   +
   +  return (
   +    <div>
   +      <h2>Hello, {name}!</h2>
   +      <button onClick={onClicked} style={{ cursor: "pointer" }}>
   +        Clicked {numClicks} times
   +      </button>
   +      {items && items.length > 0 && (
   +        <ul>
   +          {items.map((item) => (
   +            <li
   +              key={item}
   +              onClick={() => onItemSelected(item)}
   +              style={{
   +                cursor: "pointer",
   +                background:
   +                  selectedItem === item
   +                    ? "var(--st-primary-color)"
   +                    : "var(--st-secondary-background-color)",
   +              }}
   +            >
   +              {item}
   +            </li>
   +          ))}
   +        </ul>
   +      )}
   +    </div>
   +  );
   =};
   =
   =export default MyComponent;
   ```
2. In `my_react_counter/frontend/src/index.tsx`, make the following changes to pass the new props:

   ```
   => = (args) => {
   -  const { data, parentElement, setStateValue } = args;
   +  const { data, parentElement, setStateValue, setTriggerValue } = args;
   ```

   ```
   -  const { name } = data;
   +  const { name, items } = data;
   =
   =  reactRoot.render(
   =    <StrictMode>
   -      <MyComponent name={name} setStateValue={setStateValue} />
   +      <MyComponent
   +        name={name}
   +        items={items}
   +        setStateValue={setStateValue}
   +        setTriggerValue={setTriggerValue}
   +      />
   =    </StrictMode>,
   =  );
   ```
3. In `my_react_counter/__init__.py`, make the following changes to pass items and handle the new callbacks:

   ```
   -def on_num_clicks_change():
   -    pass
   -
   -
   -def my_react_counter(name, key=None):
   +def my_react_counter(name, items=None, key=None, on_item_clicked=lambda: None):
   =    component_value = out(
   -        name=name,
   =        key=key,
   -        default={"num_clicks": 0},
   -        data={"name": name},
   -        on_num_clicks_change=on_num_clicks_change,
   +        default={"num_clicks": 0, "selected_item": None},
   +        data={"name": name, "items": items or []},
   +        on_num_clicks_change=lambda: None,
   +        on_selected_item_change=lambda: None,
   +        on_item_clicked_change=on_item_clicked,
   =    )
   =    return component_value
   ```

   The wrapper now accepts `items` and an `on_item_clicked` callback (defaulting to `lambda: None`). Inside, `on_num_clicks_change` and `on_selected_item_change` use inline lambdas since nothing needs to happen for those events. `on_item_clicked_change` passes through the caller's callback so the app can react when an item is clicked.
4. To exercise the new list feature, replace the contents of `example.py` with the following:

   ```
   import streamlit as st
   from my_react_counter import my_react_counter

   st.title("My React Counter")

   result = my_react_counter(
       "Streamlit",
       items=["Python", "TypeScript", "React", "Vite"],
       key="counter",
   )

   st.write(f"Click count: {result.num_clicks}")
   if result.selected_item:
       st.write(f"Selected: {result.selected_item}")
   if result.item_clicked:
       st.write(f"Just clicked: {result.item_clicked}")
   ```
5. If `npm run dev` is still running, the frontend rebuilds automatically. Save your files, refresh your Streamlit app, and view the updated component with a clickable list.

When you're ready to share your component, create a production build.

1. Stop the `npm run dev` watcher and the `streamlit run` process by pressing `Ctrl+C` in each terminal.
2. In either terminal, navigate to the frontend directory and build the frontend:

   ```
   cd my-react-counter/my_react_counter/frontend
   npm run build
   ```
3. Navigate to the project root and build the Python wheel:

   ```
   cd ../..
   uv build
   ```

   This creates a `.whl` file in the `dist/` directory that you can distribute or upload to PyPI. For publishing instructions, see [Publish a Component](/develop/concepts/custom-components/publish).

- Learn more about the project structure in [Package-based components](/develop/concepts/custom-components/components-v2/package-based).
- Understand [State vs trigger values](/develop/concepts/custom-components/components-v2/state-and-triggers) for interactive components.
- Explore [Theming and styling](/develop/concepts/custom-components/components-v2/theming) to use Streamlit's CSS custom properties.
- Try the [Pure TypeScript tutorial](/develop/tutorials/custom-components/template-typescript) if you want a lighter-weight approach without React.

[*arrow\_back*Previous: Create a component with Pure TypeScript](/develop/tutorials/custom-components/template-typescript)[*arrow\_forward*Next: Multipage apps](/develop/tutorials/multipage)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI