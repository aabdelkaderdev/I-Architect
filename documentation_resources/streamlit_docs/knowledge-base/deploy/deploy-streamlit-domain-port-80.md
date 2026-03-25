<!-- Source: https://docs.streamlit.io/knowledge-base/deploy/deploy-streamlit-domain-port-80 -->

You want to deploy a Streamlit app on a domain so it appears to run on port 80.

- You should use a **reverse proxy** to forward requests from a webserver like [Apache](https://httpd.apache.org/) or [Nginx](https://www.nginx.com/) to the port where your Streamlit app is running. You can accomplish this in several different ways. The simplest way is to [forward all requests sent to your domain](https://discuss.streamlit.io/t/permission-denied-in-ec2-port-80/798/3) so that your Streamlit app appears as the content of your website.
- Another approach is to configure your webserver to forward requests to designated subfolders (e.g. *<http://awesomestuff.net/streamlitapp>*) to different Streamlit apps on the same domain, as in this [example config for Nginx](https://discuss.streamlit.io/t/how-to-use-streamlit-with-nginx/378/7) submitted by a Streamlit community member.

Related forum posts:

- <https://discuss.streamlit.io/t/permission-denied-in-ec2-port-80/798/3>
- <https://discuss.streamlit.io/t/how-to-use-streamlit-with-nginx/378/7>

[*arrow\_back*Previous: How can I deploy multiple Streamlit apps on different subdomains?](/knowledge-base/deploy/deploy-multiple-streamlit-apps-different-subdomains)[*arrow\_forward*Next: Does Streamlit support the WSGI Protocol? (aka Can I deploy Streamlit with gunicorn?)](/knowledge-base/deploy/does-streamlit-support-wsgi-protocol)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI