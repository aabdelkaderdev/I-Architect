<!-- Source: https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest -->

Show API reference for

Version v1.55.0*expand\_more*

# 

| Class description[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L100 "View st.AppTest source code on GitHub") | |
| --- | --- |
| st.testing.v1.AppTest(script\_path, \*, default\_timeout, args=None, kwargs=None) | |
|  |  |
| --- | --- |
| Methods | |
| [get](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestget)(element\_type) | Get elements or widgets of the specified type. |
| [run](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestrun)(\*, timeout=None) | Run the script from the current state. |
| [switch\_page](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestswitch_page)(page\_path) | Switch to another page of the app. |
| Attributes | |
| secrets (dict[str, Any]) | Dictionary of secrets to be used the simulated app. Use dict-like syntax to set secret values for the simulated app. |
| session\_state (SafeSessionState) | Session State for the simulated app. SafeSessionState object supports read and write operations as usual for Streamlit apps. |
| query\_params (dict[str, Any]) | Dictionary of query parameters to be used by the simluated app. Use dict-like syntax to set query\_params values for the simulated app. |
| [button](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestbutton) | Sequence of all st.button and st.form\_submit\_button widgets. |
| [button\_group](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestbutton_group) | Sequence of all st.pills and st.segmented\_control widgets. |
| [caption](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestcaption) | Sequence of all st.caption elements. |
| [chat\_input](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestchat_input) | Sequence of all st.chat\_input widgets. |
| [chat\_message](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestchat_message) | Sequence of all st.chat\_message elements. |
| [checkbox](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestcheckbox) | Sequence of all st.checkbox widgets. |
| [code](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestcode) | Sequence of all st.code elements. |
| [color\_picker](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestcolor_picker) | Sequence of all st.color\_picker widgets. |
| [columns](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestcolumns) | Sequence of all columns within st.columns elements. |
| [dataframe](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestdataframe) | Sequence of all st.dataframe elements. |
| [date\_input](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestdate_input) | Sequence of all st.date\_input widgets. |
| [datetime\_input](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestdatetime_input) | Sequence of all st.datetime\_input widgets. |
| [divider](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestdivider) | Sequence of all st.divider elements. |
| [error](/develop/api-reference/app-testing/st.testing.v1.apptest#apptesterror) | Sequence of all st.error elements. |
| [exception](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestexception) | Sequence of all st.exception elements. |
| [expander](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestexpander) | Sequence of all st.expander elements. |
| [feedback](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestfeedback) | Sequence of all st.feedback widgets. |
| [header](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestheader) | Sequence of all st.header elements. |
| [info](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestinfo) | Sequence of all st.info elements. |
| [json](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestjson) | Sequence of all st.json elements. |
| [latex](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestlatex) | Sequence of all st.latex elements. |
| [main](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestmain) | Sequence of elements within the main body of the app. |
| [markdown](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestmarkdown) | Sequence of all st.markdown elements. |
| [metric](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestmetric) | Sequence of all st.metric elements. |
| [multiselect](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestmultiselect) | Sequence of all st.multiselect widgets. |
| [number\_input](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestnumber_input) | Sequence of all st.number\_input widgets. |
| [radio](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestradio) | Sequence of all st.radio widgets. |
| [select\_slider](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestselect_slider) | Sequence of all st.select\_slider widgets. |
| [selectbox](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestselectbox) | Sequence of all st.selectbox widgets. |
| [sidebar](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestsidebar) | Sequence of all elements within st.sidebar. |
| [slider](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestslider) | Sequence of all st.slider widgets. |
| [status](/develop/api-reference/app-testing/st.testing.v1.apptest#appteststatus) | Sequence of all st.status elements. |
| [subheader](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestsubheader) | Sequence of all st.subheader elements. |
| [success](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestsuccess) | Sequence of all st.success elements. |
| [table](/develop/api-reference/app-testing/st.testing.v1.apptest#apptesttable) | Sequence of all st.table elements. |
| [tabs](/develop/api-reference/app-testing/st.testing.v1.apptest#apptesttabs) | Sequence of all tabs within st.tabs elements. |
| [text](/develop/api-reference/app-testing/st.testing.v1.apptest#apptesttext) | Sequence of all st.text elements. |
| [text\_area](/develop/api-reference/app-testing/st.testing.v1.apptest#apptesttext_area) | Sequence of all st.text\_area widgets. |
| [text\_input](/develop/api-reference/app-testing/st.testing.v1.apptest#apptesttext_input) | Sequence of all st.text\_input widgets. |
| [time\_input](/develop/api-reference/app-testing/st.testing.v1.apptest#apptesttime_input) | Sequence of all st.time\_input widgets. |
| [title](/develop/api-reference/app-testing/st.testing.v1.apptest#apptesttitle) | Sequence of all st.title elements. |
| [toast](/develop/api-reference/app-testing/st.testing.v1.apptest#apptesttoast) | Sequence of all st.toast elements. |
| [toggle](/develop/api-reference/app-testing/st.testing.v1.apptest#apptesttoggle) | Sequence of all st.toggle widgets. |
| [warning](/develop/api-reference/app-testing/st.testing.v1.apptest#apptestwarning) | Sequence of all st.warning elements. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L277 "View st.from_file source code on GitHub") | |
| --- | --- |
| AppTest.from\_file(cls, script\_path, \*, default\_timeout=3) | |
| Parameters | |
| script\_path (str | Path) | Path to a script file. The path should be absolute or relative to the file calling .from\_file. |
| default\_timeout (float) | Default time in seconds before a script run is timed out. Can be overridden for individual .run() calls. |
|  |  |
| --- | --- |
| Returns | |
| (AppTest) | A simulated Streamlit app for testing. The simulated app can be executed via .run(). |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L180 "View st.from_string source code on GitHub") | |
| --- | --- |
| AppTest.from\_string(cls, script, \*, default\_timeout=3) | |
| Parameters | |
| script (str) | The string contents of the script to be run. |
| default\_timeout (float) | Default time in seconds before a script run is timed out. Can be overridden for individual .run() calls. |
|  |  |
| --- | --- |
| Returns | |
| (AppTest) | A simulated Streamlit app for testing. The simulated app can be executed via .run(). |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L227 "View st.from_function source code on GitHub") | |
| --- | --- |
| AppTest.from\_function(cls, script, \*, default\_timeout=3, args=None, kwargs=None) | |
| Parameters | |
| script (Callable) | A function whose body will be used as a script. Must be runnable in isolation, so it must include any necessary imports. |
| default\_timeout (float) | Default time in seconds before a script run is timed out. Can be overridden for individual .run() calls. |
| args (tuple) | An optional tuple of args to pass to the script function. |
| kwargs (dict) | An optional dict of kwargs to pass to the script function. |
|  |  |
| --- | --- |
| Returns | |
| (AppTest) | A simulated Streamlit app for testing. The simulated app can be executed via .run(). |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L377 "View st.run source code on GitHub") | |
| --- | --- |
| AppTest.run(\*, timeout=None) | |
| Parameters | |
| timeout (float or None) | The maximum number of seconds to run the script. If timeout is None (default), Streamlit uses the default timeout set for the instance of AppTest. |
|  |  |
| --- | --- |
| Returns | |
| (AppTest) | self |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L400 "View st.switch_page source code on GitHub") | |
| --- | --- |
| AppTest.switch\_page(page\_path) | |
| Parameters | |
| page\_path (str) | Path of the page to switch to. The path must be relative to the main script's location (e.g. "pages/my\_page.py"). |
|  |  |
| --- | --- |
| Returns | |
| (AppTest) | self |

The main value of `AppTest` is providing an API to programmatically inspect and interact with the elements and widgets produced by a running Streamlit app. Using the `AppTest.<element type>` properties or `AppTest.get()` method returns a collection of all the elements or widgets of the specified type that would have been displayed by running the app.

Note that you can also retrieve elements within a specific container in the same way - first retrieve the container, then retrieve the elements just in that container.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L1063 "View st.get source code on GitHub") | |
| --- | --- |
| AppTest.get(element\_type) | |
| Parameters | |
| element\_type (str) | An element attribute of AppTest. For example, "button", "caption", or "chat\_input". |
|  |  |
| --- | --- |
| Returns | |
| (Sequence of Elements) | Sequence of elements of the given type. Individual elements can be accessed from a Sequence by index (order on the page). When getting and element\_type that is a widget, individual widgets can be accessed by key. For example, at.get("text")[0] for the first st.text element or at.get("slider")(key="my\_key") for the st.slider widget with a given key. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L455 "View st.button source code on GitHub") | |
| --- | --- |
| AppTest.button | |
|  |  |
| --- | --- |
| Returns | |
| (WidgetList of Button) | Sequence of all st.button and st.form\_submit\_button widgets. Individual widgets can be accessed from a WidgetList by index (order on the page) or key. For example, at.button[0] for the first widget or at.button(key="my\_key") for a widget with a given key. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L485 "View st.caption source code on GitHub") | |
| --- | --- |
| AppTest.caption | |
|  |  |
| --- | --- |
| Returns | |
| (ElementList of Caption) | Sequence of all st.caption elements. Individual elements can be accessed from an ElementList by index (order on the page). For example, at.caption[0] for the first element. Caption is an extension of the Element class. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L499 "View st.chat_input source code on GitHub") | |
| --- | --- |
| AppTest.chat\_input | |
|  |  |
| --- | --- |
| Returns | |
| (WidgetList of ChatInput) | Sequence of all st.chat\_input widgets. Individual widgets can be accessed from a WidgetList by index (order on the page) or key. For example, at.chat\_input[0] for the first widget or at.chat\_input(key="my\_key") for a widget with a given key. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L513 "View st.chat_message source code on GitHub") | |
| --- | --- |
| AppTest.chat\_message | |
|  |  |
| --- | --- |
| Returns | |
| (Sequence of ChatMessage) | Sequence of all st.chat\_message elements. Individual elements can be accessed from an ElementList by index (order on the page). For example, at.chat\_message[0] for the first element. ChatMessage is an extension of the Block class. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L527 "View st.checkbox source code on GitHub") | |
| --- | --- |
| AppTest.checkbox | |
|  |  |
| --- | --- |
| Returns | |
| (WidgetList of Checkbox) | Sequence of all st.checkbox widgets. Individual widgets can be accessed from a WidgetList by index (order on the page) or key. For example, at.checkbox[0] for the first widget or at.checkbox(key="my\_key") for a widget with a given key. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L541 "View st.code source code on GitHub") | |
| --- | --- |
| AppTest.code | |
|  |  |
| --- | --- |
| Returns | |
| (ElementList of Code) | Sequence of all st.code elements. Individual elements can be accessed from an ElementList by index (order on the page). For example, at.code[0] for the first element. Code is an extension of the Element class. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L555 "View st.color_picker source code on GitHub") | |
| --- | --- |
| AppTest.color\_picker | |
|  |  |
| --- | --- |
| Returns | |
| (WidgetList of ColorPicker) | Sequence of all st.color\_picker widgets. Individual widgets can be accessed from a WidgetList by index (order on the page) or key. For example, at.color\_picker[0] for the first widget or at.color\_picker(key="my\_key") for a widget with a given key. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L569 "View st.columns source code on GitHub") | |
| --- | --- |
| AppTest.columns | |
|  |  |
| --- | --- |
| Returns | |
| (Sequence of Column) | Sequence of all columns within st.columns elements. Individual columns can be accessed from an ElementList by index (order on the page). For example, at.columns[0] for the first column. Column is an extension of the Block class. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L586 "View st.dataframe source code on GitHub") | |
| --- | --- |
| AppTest.dataframe | |
|  |  |
| --- | --- |
| Returns | |
| (ElementList of Dataframe) | Sequence of all st.dataframe elements. Individual elements can be accessed from an ElementList by index (order on the page). For example, at.dataframe[0] for the first element. Dataframe is an extension of the Element class. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L600 "View st.date_input source code on GitHub") | |
| --- | --- |
| AppTest.date\_input | |
|  |  |
| --- | --- |
| Returns | |
| (WidgetList of DateInput) | Sequence of all st.date\_input widgets. Individual widgets can be accessed from a WidgetList by index (order on the page) or key. For example, at.date\_input[0] for the first widget or at.date\_input(key="my\_key") for a widget with a given key. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L628 "View st.divider source code on GitHub") | |
| --- | --- |
| AppTest.divider | |
|  |  |
| --- | --- |
| Returns | |
| (ElementList of Divider) | Sequence of all st.divider elements. Individual elements can be accessed from an ElementList by index (order on the page). For example, at.divider[0] for the first element. Divider is an extension of the Element class. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L642 "View st.error source code on GitHub") | |
| --- | --- |
| AppTest.error | |
|  |  |
| --- | --- |
| Returns | |
| (ElementList of Error) | Sequence of all st.error elements. Individual elements can be accessed from an ElementList by index (order on the page). For example, at.error[0] for the first element. Error is an extension of the Element class. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L656 "View st.exception source code on GitHub") | |
| --- | --- |
| AppTest.exception | |
|  |  |
| --- | --- |
| Returns | |
| (ElementList of Exception) | Sequence of all st.exception elements. Individual elements can be accessed from an ElementList by index (order on the page). For example, at.exception[0] for the first element. Exception is an extension of the Element class. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L684 "View st.expander source code on GitHub") | |
| --- | --- |
| AppTest.expander | |
|  |  |
| --- | --- |
| Returns | |
| (Sequence of Expandable) | Sequence of all st.expander elements. Individual elements can be accessed from a Sequence by index (order on the page). For example, at.expander[0] for the first element. Expandable is an extension of the Block class. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L698 "View st.header source code on GitHub") | |
| --- | --- |
| AppTest.header | |
|  |  |
| --- | --- |
| Returns | |
| (ElementList of Header) | Sequence of all st.header elements. Individual elements can be accessed from an ElementList by index (order on the page). For example, at.header[0] for the first element. Header is an extension of the Element class. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L712 "View st.info source code on GitHub") | |
| --- | --- |
| AppTest.info | |
|  |  |
| --- | --- |
| Returns | |
| (ElementList of Info) | Sequence of all st.info elements. Individual elements can be accessed from an ElementList by index (order on the page). For example, at.info[0] for the first element. Info is an extension of the Element class. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L726 "View st.json source code on GitHub") | |
| --- | --- |
| AppTest.json | |
|  |  |
| --- | --- |
| Returns | |
| (ElementList of Json) | Sequence of all st.json elements. Individual elements can be accessed from an ElementList by index (order on the page). For example, at.json[0] for the first element. Json is an extension of the Element class. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L740 "View st.latex source code on GitHub") | |
| --- | --- |
| AppTest.latex | |
|  |  |
| --- | --- |
| Returns | |
| (ElementList of Latex) | Sequence of all st.latex elements. Individual elements can be accessed from an ElementList by index (order on the page). For example, at.latex[0] for the first element. Latex is an extension of the Element class. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L429 "View st.main source code on GitHub") | |
| --- | --- |
| AppTest.main | |
|  |  |
| --- | --- |
| Returns | |
| (Block) | A container of elements. Block can be queried for elements in the same manner as AppTest. For example, Block.checkbox will return all st.checkbox within the associated container. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L754 "View st.markdown source code on GitHub") | |
| --- | --- |
| AppTest.markdown | |
|  |  |
| --- | --- |
| Returns | |
| (ElementList of Markdown) | Sequence of all st.markdown elements. Individual elements can be accessed from an ElementList by index (order on the page). For example, at.markdown[0] for the first element. Markdown is an extension of the Element class. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L768 "View st.metric source code on GitHub") | |
| --- | --- |
| AppTest.metric | |
|  |  |
| --- | --- |
| Returns | |
| (ElementList of Metric) | Sequence of all st.metric elements. Individual elements can be accessed from an ElementList by index (order on the page). For example, at.metric[0] for the first element. Metric is an extension of the Element class. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L782 "View st.multiselect source code on GitHub") | |
| --- | --- |
| AppTest.multiselect | |
|  |  |
| --- | --- |
| Returns | |
| (WidgetList of Multiselect) | Sequence of all st.multiselect widgets. Individual widgets can be accessed from a WidgetList by index (order on the page) or key. For example, at.multiselect[0] for the first widget or at.multiselect(key="my\_key") for a widget with a given key. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L796 "View st.number_input source code on GitHub") | |
| --- | --- |
| AppTest.number\_input | |
|  |  |
| --- | --- |
| Returns | |
| (WidgetList of NumberInput) | Sequence of all st.number\_input widgets. Individual widgets can be accessed from a WidgetList by index (order on the page) or key. For example, at.number\_input[0] for the first widget or at.number\_input(key="my\_key") for a widget with a given key. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L810 "View st.radio source code on GitHub") | |
| --- | --- |
| AppTest.radio | |
|  |  |
| --- | --- |
| Returns | |
| (WidgetList of Radio) | Sequence of all st.radio widgets. Individual widgets can be accessed from a WidgetList by index (order on the page) or key. For example, at.radio[0] for the first widget or at.radio(key="my\_key") for a widget with a given key. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L824 "View st.select_slider source code on GitHub") | |
| --- | --- |
| AppTest.select\_slider | |
|  |  |
| --- | --- |
| Returns | |
| (WidgetList of SelectSlider) | Sequence of all st.select\_slider widgets. Individual widgets can be accessed from a WidgetList by index (order on the page) or key. For example, at.select\_slider[0] for the first widget or at.select\_slider(key="my\_key") for a widget with a given key. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L838 "View st.selectbox source code on GitHub") | |
| --- | --- |
| AppTest.selectbox | |
|  |  |
| --- | --- |
| Returns | |
| (WidgetList of Selectbox) | Sequence of all st.selectbox widgets. Individual widgets can be accessed from a WidgetList by index (order on the page) or key. For example, at.selectbox[0] for the first widget or at.selectbox(key="my\_key") for a widget with a given key. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L442 "View st.sidebar source code on GitHub") | |
| --- | --- |
| AppTest.sidebar | |
|  |  |
| --- | --- |
| Returns | |
| (Block) | A container of elements. Block can be queried for elements in the same manner as AppTest. For example, Block.checkbox will return all st.checkbox within the associated container. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L852 "View st.slider source code on GitHub") | |
| --- | --- |
| AppTest.slider | |
|  |  |
| --- | --- |
| Returns | |
| (WidgetList of Slider) | Sequence of all st.slider widgets. Individual widgets can be accessed from a WidgetList by index (order on the page) or key. For example, at.slider[0] for the first widget or at.slider(key="my\_key") for a widget with a given key. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L866 "View st.subheader source code on GitHub") | |
| --- | --- |
| AppTest.subheader | |
|  |  |
| --- | --- |
| Returns | |
| (ElementList of Subheader) | Sequence of all st.subheader elements. Individual elements can be accessed from an ElementList by index (order on the page). For example, at.subheader[0] for the first element. Subheader is an extension of the Element class. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L880 "View st.success source code on GitHub") | |
| --- | --- |
| AppTest.success | |
|  |  |
| --- | --- |
| Returns | |
| (ElementList of Success) | Sequence of all st.success elements. Individual elements can be accessed from an ElementList by index (order on the page). For example, at.success[0] for the first element. Success is an extension of the Element class. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L894 "View st.status source code on GitHub") | |
| --- | --- |
| AppTest.status | |
|  |  |
| --- | --- |
| Returns | |
| (Sequence of Status) | Sequence of all st.status elements. Individual elements can be accessed from a Sequence by index (order on the page). For example, at.status[0] for the first element. Status is an extension of the Block class. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L908 "View st.table source code on GitHub") | |
| --- | --- |
| AppTest.table | |
|  |  |
| --- | --- |
| Returns | |
| (ElementList of Table) | Sequence of all st.table elements. Individual elements can be accessed from an ElementList by index (order on the page). For example, at.table[0] for the first element. Table is an extension of the Element class. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L922 "View st.tabs source code on GitHub") | |
| --- | --- |
| AppTest.tabs | |
|  |  |
| --- | --- |
| Returns | |
| (Sequence of Tab) | Sequence of all tabs within st.tabs elements. Individual tabs can be accessed from an ElementList by index (order on the page). For example, at.tabs[0] for the first tab. Tab is an extension of the Block class. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L942 "View st.text source code on GitHub") | |
| --- | --- |
| AppTest.text | |
|  |  |
| --- | --- |
| Returns | |
| (ElementList of Text) | Sequence of all st.text elements. Individual elements can be accessed from an ElementList by index (order on the page). For example, at.text[0] for the first element. Text is an extension of the Element class. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L956 "View st.text_area source code on GitHub") | |
| --- | --- |
| AppTest.text\_area | |
|  |  |
| --- | --- |
| Returns | |
| (WidgetList of TextArea) | Sequence of all st.text\_area widgets. Individual widgets can be accessed from a WidgetList by index (order on the page) or key. For example, at.text\_area[0] for the first widget or at.text\_area(key="my\_key") for a widget with a given key. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L970 "View st.text_input source code on GitHub") | |
| --- | --- |
| AppTest.text\_input | |
|  |  |
| --- | --- |
| Returns | |
| (WidgetList of TextInput) | Sequence of all st.text\_input widgets. Individual widgets can be accessed from a WidgetList by index (order on the page) or key. For example, at.text\_input[0] for the first widget or at.text\_input(key="my\_key") for a widget with a given key. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L984 "View st.time_input source code on GitHub") | |
| --- | --- |
| AppTest.time\_input | |
|  |  |
| --- | --- |
| Returns | |
| (WidgetList of TimeInput) | Sequence of all st.time\_input widgets. Individual widgets can be accessed from a WidgetList by index (order on the page) or key. For example, at.time\_input[0] for the first widget or at.time\_input(key="my\_key") for a widget with a given key. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L998 "View st.title source code on GitHub") | |
| --- | --- |
| AppTest.title | |
|  |  |
| --- | --- |
| Returns | |
| (ElementList of Title) | Sequence of all st.title elements. Individual elements can be accessed from an ElementList by index (order on the page). For example, at.title[0] for the first element. Title is an extension of the Element class. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L1012 "View st.toast source code on GitHub") | |
| --- | --- |
| AppTest.toast | |
|  |  |
| --- | --- |
| Returns | |
| (ElementList of Toast) | Sequence of all st.toast elements. Individual elements can be accessed from an ElementList by index (order on the page). For example, at.toast[0] for the first element. Toast is an extension of the Element class. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L1026 "View st.toggle source code on GitHub") | |
| --- | --- |
| AppTest.toggle | |
|  |  |
| --- | --- |
| Returns | |
| (WidgetList of Toggle) | Sequence of all st.toggle widgets. Individual widgets can be accessed from a WidgetList by index (order on the page) or key. For example, at.toggle[0] for the first widget or at.toggle(key="my\_key") for a widget with a given key. |

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/app_test.py#L1040 "View st.warning source code on GitHub") | |
| --- | --- |
| AppTest.warning | |
|  |  |
| --- | --- |
| Returns | |
| (ElementList of Warning) | Sequence of all st.warning elements. Individual elements can be accessed from an ElementList by index (order on the page). For example, at.warning[0] for the first element. Warning is an extension of the Element class. |

[*arrow\_back*Previous: App testing](/develop/api-reference/app-testing)[*arrow\_forward*Next: element\_tree](/develop/api-reference/app-testing/testing-element-classes)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI