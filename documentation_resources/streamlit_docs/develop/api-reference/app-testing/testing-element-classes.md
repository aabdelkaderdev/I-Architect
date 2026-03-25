<!-- Source: https://docs.streamlit.io/develop/api-reference/app-testing/testing-element-classes -->

Show API reference for

Version v1.55.0*expand\_more*

The `Block` class has the same methods and attributes as `AppTest`. A `Block` instance represents a container of elements just as `AppTest` represents the entire app. For example, `Block.button` will produce a `WidgetList` of `Button` in the same manner as [`AppTest.button`](/develop/api-reference/testing/st.testing.v1.apptest#apptestbutton).

`ChatMessage`, `Column`, and `Tab` all inherit from `Block`. For all container classes, parameters of the original element can be obtained as properties. For example, `ChatMessage.avatar` and `Tab.label`.

| Class description[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/element_tree.py#L107 "View st.Element source code on GitHub") | |
| --- | --- |
| st.testing.v1.element\_tree.Element(proto, root) | |
|  |  |
| --- | --- |
| Methods | |
| [run](/develop/api-reference/app-testing/testing-element-classes#elementrun)(\*, timeout=None) | Run the AppTest script which contains the element. |
| Attributes | |
| [value](/develop/api-reference/app-testing/testing-element-classes#elementvalue) | The value or contents of the element. |

| Class description[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/element_tree.py#L306 "View st.Button source code on GitHub") | |
| --- | --- |
| st.testing.v1.element\_tree.Button(proto, root) | |
|  |  |
| --- | --- |
| Methods | |
| [click](/develop/api-reference/app-testing/testing-element-classes#buttonclick)() | Set the value of the button to True. |
| [run](/develop/api-reference/app-testing/testing-element-classes#buttonrun)(\*, timeout=None) | Run the AppTest script which contains the element. |
| [set\_value](/develop/api-reference/app-testing/testing-element-classes#buttonset_value)(v) | Set the value of the button. |
| Attributes | |
| [value](/develop/api-reference/app-testing/testing-element-classes#buttonvalue) | The value of the button. (bool) |

| Class description[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/element_tree.py#L348 "View st.ChatInput source code on GitHub") | |
| --- | --- |
| st.testing.v1.element\_tree.ChatInput(proto, root) | |
|  |  |
| --- | --- |
| Methods | |
| [run](/develop/api-reference/app-testing/testing-element-classes#chatinputrun)(\*, timeout=None) | Run the AppTest script which contains the element. |
| [set\_value](/develop/api-reference/app-testing/testing-element-classes#chatinputset_value)(v) | Set the value of the widget. |
| Attributes | |
| [value](/develop/api-reference/app-testing/testing-element-classes#chatinputvalue) | The value of the widget. (str) |

| Class description[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/element_tree.py#L383 "View st.Checkbox source code on GitHub") | |
| --- | --- |
| st.testing.v1.element\_tree.Checkbox(proto, root) | |
|  |  |
| --- | --- |
| Methods | |
| [check](/develop/api-reference/app-testing/testing-element-classes#checkboxcheck)() | Set the value of the widget to True. |
| [run](/develop/api-reference/app-testing/testing-element-classes#checkboxrun)(\*, timeout=None) | Run the AppTest script which contains the element. |
| [set\_value](/develop/api-reference/app-testing/testing-element-classes#checkboxset_value)(v) | Set the value of the widget. |
| [uncheck](/develop/api-reference/app-testing/testing-element-classes#checkboxuncheck)() | Set the value of the widget to False. |
| Attributes | |
| [value](/develop/api-reference/app-testing/testing-element-classes#checkboxvalue) | The value of the widget. (bool) |

| Class description[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/element_tree.py#L450 "View st.ColorPicker source code on GitHub") | |
| --- | --- |
| st.testing.v1.element\_tree.ColorPicker(proto, root) | |
|  |  |
| --- | --- |
| Methods | |
| [pick](/develop/api-reference/app-testing/testing-element-classes#colorpickerpick)(v) | Set the value of the widget as a hex string. May omit the "#" prefix. |
| [run](/develop/api-reference/app-testing/testing-element-classes#colorpickerrun)(\*, timeout=None) | Run the AppTest script which contains the element. |
| [set\_value](/develop/api-reference/app-testing/testing-element-classes#colorpickerset_value)(v) | Set the value of the widget as a hex string. |
| Attributes | |
| [value](/develop/api-reference/app-testing/testing-element-classes#colorpickervalue) | The currently selected value as a hex string. (str) |

| Class description[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/element_tree.py#L518 "View st.DateInput source code on GitHub") | |
| --- | --- |
| st.testing.v1.element\_tree.DateInput(proto, root) | |
|  |  |
| --- | --- |
| Methods | |
| [run](/develop/api-reference/app-testing/testing-element-classes#dateinputrun)(\*, timeout=None) | Run the AppTest script which contains the element. |
| [set\_value](/develop/api-reference/app-testing/testing-element-classes#dateinputset_value)(v) | Set the value of the widget. |
| Attributes | |
| [value](/develop/api-reference/app-testing/testing-element-classes#dateinputvalue) | The value of the widget. (date or Tuple of date) |

| Class description[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/element_tree.py#L882 "View st.Multiselect source code on GitHub") | |
| --- | --- |
| st.testing.v1.element\_tree.Multiselect(proto, root) | |
|  |  |
| --- | --- |
| Methods | |
| [run](/develop/api-reference/app-testing/testing-element-classes#multiselectrun)(\*, timeout=None) | Run the AppTest script which contains the element. |
| [select](/develop/api-reference/app-testing/testing-element-classes#multiselectselect)(v) | Add a selection to the widget. Do nothing if the value is already selected. If testing a multiselect widget with repeated options, use set\_value instead. |
| [set\_value](/develop/api-reference/app-testing/testing-element-classes#multiselectset_value)(v) | Set the value of the multiselect widget. (list) |
| [unselect](/develop/api-reference/app-testing/testing-element-classes#multiselectunselect)(v) | Remove a selection from the widget. Do nothing if the value is not already selected. If a value is selected multiple times, the first instance is removed. |
| Attributes | |
| [format\_func](/develop/api-reference/app-testing/testing-element-classes#multiselectformat_func) | The widget's formatting function for displaying options. (callable) |
| [indices](/develop/api-reference/app-testing/testing-element-classes#multiselectindices) | The indices of the currently selected values from the options. (list) |
| [value](/develop/api-reference/app-testing/testing-element-classes#multiselectvalue) | The currently selected values from the options. (list) |
| [values](/develop/api-reference/app-testing/testing-element-classes#multiselectvalues) | The currently selected values from the options. (list) |

| Class description[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/element_tree.py#L975 "View st.NumberInput source code on GitHub") | |
| --- | --- |
| st.testing.v1.element\_tree.NumberInput(proto, root) | |
|  |  |
| --- | --- |
| Methods | |
| [decrement](/develop/api-reference/app-testing/testing-element-classes#numberinputdecrement)() | Decrement the st.number\_input widget as if the user clicked "-". |
| [increment](/develop/api-reference/app-testing/testing-element-classes#numberinputincrement)() | Increment the st.number\_input widget as if the user clicked "+". |
| [run](/develop/api-reference/app-testing/testing-element-classes#numberinputrun)(\*, timeout=None) | Run the AppTest script which contains the element. |
| [set\_value](/develop/api-reference/app-testing/testing-element-classes#numberinputset_value)(v) | Set the value of the st.number\_input widget. |
| Attributes | |
| [value](/develop/api-reference/app-testing/testing-element-classes#numberinputvalue) | Get the current value of the st.number\_input widget. |

| Class description[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/element_tree.py#L1036 "View st.Radio source code on GitHub") | |
| --- | --- |
| st.testing.v1.element\_tree.Radio(proto, root) | |
|  |  |
| --- | --- |
| Methods | |
| [run](/develop/api-reference/app-testing/testing-element-classes#radiorun)(\*, timeout=None) | Run the AppTest script which contains the element. |
| [set\_value](/develop/api-reference/app-testing/testing-element-classes#radioset_value)(v) | Set the selection by value. |
| Attributes | |
| [format\_func](/develop/api-reference/app-testing/testing-element-classes#radioformat_func) | The widget's formatting function for displaying options. (callable) |
| [index](/develop/api-reference/app-testing/testing-element-classes#radioindex) | The index of the current selection. (int) |
| [value](/develop/api-reference/app-testing/testing-element-classes#radiovalue) | The currently selected value from the options. (Any) |

| Class description[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/element_tree.py#L1166 "View st.SelectSlider source code on GitHub") | |
| --- | --- |
| st.testing.v1.element\_tree.SelectSlider(proto, root) | |
|  |  |
| --- | --- |
| Methods | |
| [run](/develop/api-reference/app-testing/testing-element-classes#selectsliderrun)(\*, timeout=None) | Run the AppTest script which contains the element. |
| [set\_range](/develop/api-reference/app-testing/testing-element-classes#selectsliderset_range)(lower, upper) | Set the ranged selection by values. |
| [set\_value](/develop/api-reference/app-testing/testing-element-classes#selectsliderset_value)(v) | Set the (single) selection by value. |
| Attributes | |
| [format\_func](/develop/api-reference/app-testing/testing-element-classes#selectsliderformat_func) | The widget's formatting function for displaying options. (callable) |
| [value](/develop/api-reference/app-testing/testing-element-classes#selectslidervalue) | The currently selected value or range. (Any or Sequence of Any) |

| Class description[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/element_tree.py#L1095 "View st.Selectbox source code on GitHub") | |
| --- | --- |
| st.testing.v1.element\_tree.Selectbox(proto, root) | |
|  |  |
| --- | --- |
| Methods | |
| [run](/develop/api-reference/app-testing/testing-element-classes#selectboxrun)(\*, timeout=None) | Run the AppTest script which contains the element. |
| [select](/develop/api-reference/app-testing/testing-element-classes#selectboxselect)(v) | Set the selection by value. |
| [select\_index](/develop/api-reference/app-testing/testing-element-classes#selectboxselect_index)(index) | Set the selection by index. |
| [set\_value](/develop/api-reference/app-testing/testing-element-classes#selectboxset_value)(v) | Set the selection by value. |
| Attributes | |
| [format\_func](/develop/api-reference/app-testing/testing-element-classes#selectboxformat_func) | The widget's formatting function for displaying options. (callable) |
| [index](/develop/api-reference/app-testing/testing-element-classes#selectboxindex) | The index of the current selection. (int) |
| [value](/develop/api-reference/app-testing/testing-element-classes#selectboxvalue) | The currently selected value from the options. (Any) |

| Class description[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/element_tree.py#L1244 "View st.Slider source code on GitHub") | |
| --- | --- |
| st.testing.v1.element\_tree.Slider(proto, root) | |
|  |  |
| --- | --- |
| Methods | |
| [run](/develop/api-reference/app-testing/testing-element-classes#sliderrun)(\*, timeout=None) | Run the AppTest script which contains the element. |
| [set\_range](/develop/api-reference/app-testing/testing-element-classes#sliderset_range)(lower, upper) | Set the ranged value of the slider. |
| [set\_value](/develop/api-reference/app-testing/testing-element-classes#sliderset_value)(v) | Set the (single) value of the slider. |
| Attributes | |
| [value](/develop/api-reference/app-testing/testing-element-classes#slidervalue) | The currently selected value or range. (Any or Sequence of Any) |

| Class description[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/element_tree.py#L1332 "View st.TextArea source code on GitHub") | |
| --- | --- |
| st.testing.v1.element\_tree.TextArea(proto, root) | |
|  |  |
| --- | --- |
| Methods | |
| [input](/develop/api-reference/app-testing/testing-element-classes#textareainput)(v) | Set the value of the widget only if the value does not exceed the maximum allowed characters. |
| [run](/develop/api-reference/app-testing/testing-element-classes#textarearun)(\*, timeout=None) | Run the AppTest script which contains the element. |
| [set\_value](/develop/api-reference/app-testing/testing-element-classes#textareaset_value)(v) | Set the value of the widget. |
| Attributes | |
| [value](/develop/api-reference/app-testing/testing-element-classes#textareavalue) | The current value of the widget. (str) |

| Class description[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/element_tree.py#L1384 "View st.TextInput source code on GitHub") | |
| --- | --- |
| st.testing.v1.element\_tree.TextInput(proto, root) | |
|  |  |
| --- | --- |
| Methods | |
| [input](/develop/api-reference/app-testing/testing-element-classes#textinputinput)(v) | Set the value of the widget only if the value does not exceed the maximum allowed characters. |
| [run](/develop/api-reference/app-testing/testing-element-classes#textinputrun)(\*, timeout=None) | Run the AppTest script which contains the element. |
| [set\_value](/develop/api-reference/app-testing/testing-element-classes#textinputset_value)(v) | Set the value of the widget. |
| Attributes | |
| [value](/develop/api-reference/app-testing/testing-element-classes#textinputvalue) | The current value of the widget. (str) |

| Class description[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/element_tree.py#L1440 "View st.TimeInput source code on GitHub") | |
| --- | --- |
| st.testing.v1.element\_tree.TimeInput(proto, root) | |
|  |  |
| --- | --- |
| Methods | |
| [decrement](/develop/api-reference/app-testing/testing-element-classes#timeinputdecrement)() | Select the previous available time. |
| [increment](/develop/api-reference/app-testing/testing-element-classes#timeinputincrement)() | Select the next available time. |
| [run](/develop/api-reference/app-testing/testing-element-classes#timeinputrun)(\*, timeout=None) | Run the AppTest script which contains the element. |
| [set\_value](/develop/api-reference/app-testing/testing-element-classes#timeinputset_value)(v) | Set the value of the widget. |
| Attributes | |
| [value](/develop/api-reference/app-testing/testing-element-classes#timeinputvalue) | The current value of the widget. (time) |

| Class description[[source]](https://github.com/streamlit/streamlit/blob/1.55.0/lib/streamlit/testing/v1/element_tree.py#L1570 "View st.Toggle source code on GitHub") | |
| --- | --- |
| st.testing.v1.element\_tree.Toggle(proto, root) | |
|  |  |
| --- | --- |
| Methods | |
| [run](/develop/api-reference/app-testing/testing-element-classes#togglerun)(\*, timeout=None) | Run the AppTest script which contains the element. |
| [set\_value](/develop/api-reference/app-testing/testing-element-classes#toggleset_value)(v) | Set the value of the widget. |
| Attributes | |
| [value](/develop/api-reference/app-testing/testing-element-classes#togglevalue) | The current value of the widget. (bool) |

[*arrow\_back*Previous: AppTest](/develop/api-reference/app-testing/st.testing.v1.apptest)[*arrow\_forward*Next: Command line](/develop/api-reference/cli)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI