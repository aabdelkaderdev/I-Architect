<!-- Source: https://docs.streamlit.io/develop/api-reference/data/st.column_config -->

When working with data in Streamlit, the `st.column_config` class is a powerful tool for configuring data display and interaction. Specifically designed for the `column_config` parameter in [`st.dataframe`](/develop/api-reference/data/st.dataframe) and [`st.data_editor`](/develop/api-reference/data/st.data_editor), it provides a suite of methods to tailor your columns to various data types - from simple text and numbers to lists, URLs, images, and more.

Whether it's translating temporal data into user-friendly formats or utilizing charts and progress bars for clearer data visualization, column configuration not only provides the user with an enriched data viewing experience but also ensures that you're equipped with the tools to present and interact with your data, just the way you want it.

[#### Column

Configure a generic column.

```
Column("Streamlit Widgets", width="medium", help="Streamlit **widget** commands 🎈")
```](/develop/api-reference/data/st.column_config/st.column_config.column)[#### Text column

Configure a text column.

```
TextColumn("Widgets", max_chars=50, validate="^st\.[a-z_]+$")
```](/develop/api-reference/data/st.column_config/st.column_config.textcolumn)[#### Number column

Configure a number column.

```
NumberColumn("Price (in USD)", min_value=0, format="$%d")
```](/develop/api-reference/data/st.column_config/st.column_config.numbercolumn)[#### Checkbox column

Configure a checkbox column.

```
CheckboxColumn("Your favorite?", help="Select your **favorite** widgets")
```](/develop/api-reference/data/st.column_config/st.column_config.checkboxcolumn)[#### Selectbox column

Configure a selectbox column.

```
SelectboxColumn("App Category", options=["🤖 LLM", "📈 Data Viz"])
```](/develop/api-reference/data/st.column_config/st.column_config.selectboxcolumn)[#### Multiselect column

Configure a multiselect column.

```
MultiselectColumn("App Category", options=["LLM", "Visualization"])
```](/develop/api-reference/data/st.column_config/st.column_config.multiselectcolumn)[#### Datetime column

Configure a datetime column.

```
DatetimeColumn("Appointment", min_value=datetime(2023, 6, 1), format="D MMM YYYY, h:mm a")
```](/develop/api-reference/data/st.column_config/st.column_config.datetimecolumn)[#### Date column

Configure a date column.

```
DateColumn("Birthday", max_value=date(2005, 1, 1), format="DD.MM.YYYY")
```](/develop/api-reference/data/st.column_config/st.column_config.datecolumn)[#### Time column

Configure a time column.

```
TimeColumn("Appointment", min_value=time(8, 0, 0), format="hh:mm a")
```](/develop/api-reference/data/st.column_config/st.column_config.timecolumn)[#### JSON column

Configure a JSON column.

```
JSONColumn("Properties", width="medium")
```](/develop/api-reference/data/st.column_config/st.column_config.jsoncolumn)[#### List column

Configure a list column.

```
ListColumn("Sales (last 6 months)", width="medium")
```](/develop/api-reference/data/st.column_config/st.column_config.listcolumn)[#### Link column

Configure a link column.

```
LinkColumn("Trending apps", max_chars=100, validate="^https://.*$")
```](/develop/api-reference/data/st.column_config/st.column_config.linkcolumn)[#### Image column

Configure an image column.

```
ImageColumn("Preview Image", help="The preview screenshots")
```](/develop/api-reference/data/st.column_config/st.column_config.imagecolumn)[#### Area chart column

Configure an area chart column.

```
AreaChartColumn("Sales (last 6 months)" y_min=0, y_max=100)
```](/develop/api-reference/data/st.column_config/st.column_config.areachartcolumn)[#### Line chart column

Configure a line chart column.

```
LineChartColumn("Sales (last 6 months)" y_min=0, y_max=100)
```](/develop/api-reference/data/st.column_config/st.column_config.linechartcolumn)[#### Bar chart column

Configure a bar chart column.

```
BarChartColumn("Marketing spend" y_min=0, y_max=100)
```](/develop/api-reference/data/st.column_config/st.column_config.barchartcolumn)[#### Progress column

Configure a progress column.

```
ProgressColumn("Sales volume", min_value=0, max_value=1000, format="$%f")
```](/develop/api-reference/data/st.column_config/st.column_config.progresscolumn)

[*arrow\_back*Previous: st.data\_editor](/develop/api-reference/data/st.data_editor)[*arrow\_forward*Next: Column](/develop/api-reference/data/st.column_config/st.column_config.column)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI