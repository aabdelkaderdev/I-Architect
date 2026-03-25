<!-- Source: https://reference.langchain.com/python/langchain-classic/callbacks/streamlit -->

Modulev1.2.13 (latest)●Since v1.0

# streamlit

## Functions

[function

StreamlitCallbackHandler

Callback Handler that writes to a Streamlit app.

This CallbackHandler is geared towards
use with a LangChain Agent; it displays the Agent's LLM and tool-usage "thoughts"
inside a series of Streamlit expanders.

## Parameters

parent\_container
The `st.container` that will contain all the Streamlit elements that the
Handler creates.
max\_thought\_containers
The max number of completed LLM thought containers to show at once. When this
threshold is reached, a new thought will cause the oldest thoughts to be
collapsed into a "History" expander.
expand\_new\_thoughts
Each LLM "thought" gets its own `st.expander`. This param controls whether that
expander is expanded by default.
collapse\_completed\_thoughts
If `True`, LLM thought expanders will be collapsed when completed.
thought\_labeler
An optional custom LLMThoughtLabeler instance. If unspecified, the handler
will use the default thought labeling logic.

## Returns:

A new StreamlitCallbackHandler instance.

Note that this is an "auto-updating" API: if the installed version of Streamlit
has a more recent StreamlitCallbackHandler implementation, an instance of that class
will be used.](/python/langchain-classic/callbacks/streamlit/StreamlitCallbackHandler)

## Modules

[module

streamlit\_callback\_handler](/python/langchain-classic/callbacks/streamlit/streamlit_callback_handler)[module

mutable\_expander](/python/langchain-classic/callbacks/streamlit/mutable_expander)


