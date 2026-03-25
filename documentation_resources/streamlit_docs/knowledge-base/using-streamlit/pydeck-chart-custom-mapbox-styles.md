<!-- Source: https://docs.streamlit.io/knowledge-base/using-streamlit/pydeck-chart-custom-mapbox-styles -->

If you are supplying a Mapbox token, but the resulting `pydeck_chart` doesn't show your custom Mapbox styles, please check that you are adding the Mapbox token to the Streamlit `config.toml` configuration file. Streamlit DOES NOT read Mapbox tokens from inside of a PyDeck specification (i.e. from inside of the Streamlit app). Please see this [forum thread](https://discuss.streamlit.io/t/deprecation-warning-deckgl-pydeck-maps-to-require-mapbox-token-for-production-usage/2982/10) for more information.

[*arrow\_back*Previous: How to insert elements out of order?](/knowledge-base/using-streamlit/insert-elements-out-of-order)[*arrow\_forward*Next: How to remove "· Streamlit" from the app title?](/knowledge-base/using-streamlit/remove-streamlit-app-title)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI