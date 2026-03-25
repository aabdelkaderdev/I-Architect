<!-- Source: https://docs.streamlit.io/knowledge-base/deploy/does-streamlit-support-wsgi-protocol -->

You're not sure whether your Streamlit app can be deployed with gunicorn.

Streamlit does not support the WSGI protocol at this time, so deploying Streamlit with (for example) gunicorn is not currently possible. Check out this [forum thread regarding deploying Streamlit in a gunicorn-like manner](https://discuss.streamlit.io/t/how-do-i-set-the-server-to-0-0-0-0-for-deployment-using-docker/216) to see how other users have accomplished this.

[*arrow\_back*Previous: How do I deploy Streamlit on a domain so it appears to run on a regular port (i.e. port 80)?](/knowledge-base/deploy/deploy-streamlit-domain-port-80)[*arrow\_forward*Next: How do I increase the upload limit of st.file\_uploader on Streamlit Community Cloud?](/knowledge-base/deploy/increase-file-uploader-limit-streamlit-cloud)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI